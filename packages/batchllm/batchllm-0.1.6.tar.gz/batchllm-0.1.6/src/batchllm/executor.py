#!/usr/bin/python
import os
import json
import threading
from queue import Queue, Empty
from absl import app
from absl import flags
from absl import logging
from odps import ODPS
from odps.tunnel import TableTunnel
from vllm import LLM, SamplingParams
from modelscope import snapshot_download

FLAGS = flags.FLAGS

# template
#flags.DEFINE_integer('age', None, 'Your age in years.', lower_bound=0)
#flags.DEFINE_float("weight", None, "Your weight in kg.", lower_bound=0)
#flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
#flags.DEFINE_enum('job', 'running', ['running', 'stopped'], 'Job status.') #DEFINE_enum()函数()中各元素分别代表name,default,enum_values,help
#flags.DEFINE_list("food", None, "Your favorite food")

# user config
flags.DEFINE_string('infer_kernel', 'SingleInfer', 'user define class for infer.')
flags.DEFINE_integer('batch_size', 1024, 'batch size.')
flags.DEFINE_integer('max_queue_len', 102400, 'max queue len.')

# odps config
flags.DEFINE_string('access_id', '', 'odps access id.')
flags.DEFINE_string('access_key', '', 'odps access key.')
flags.DEFINE_string('project', 'bi_strategy', 'odps project.')
flags.DEFINE_string('endpoint', 'http://service-corp.odps.aliyun-inc.com/api', 'odps endpoint.')

# table config
flags.DEFINE_string('input_table', '', 'Input table name.')
flags.DEFINE_string('input_partition', '', 'Input table partition name.')
flags.DEFINE_string('columns', 'prompts', 'Input table columns.')
flags.DEFINE_string('output_table', '', 'Output table name.')
flags.DEFINE_string('output_partition', '', 'Output table partition name.')
flags.DEFINE_integer('output_table_lifecycle', 14, 'Output table lifecycle.')

# LLM init config
flags.DEFINE_string('model_name', '', 'model name.')
flags.DEFINE_boolean('enable_prefix_caching', False, 'enable prefix caching.')
flags.DEFINE_float('gpu_memory_utilization', 0.9, 'cache kv.')
flags.DEFINE_integer('max_model_len', 20000, 'max tokens.')

# sampling config
flags.DEFINE_integer('max_tokens', 500, 'max tokens.')
flags.DEFINE_integer("top_k", -1, "the numbers of top tokens")
flags.DEFINE_float("top_p", 1.0, "control the cumulative prob.", lower_bound=0)


def check_config():
    if not all((FLAGS.access_id, FLAGS.access_key, FLAGS.input_table, FLAGS.input_partition)):
        logging.error(f"access_id、access_key、input_table、input_partition is null")
    if not FLAGS.output_table:
        FLAGS.output_table = FLAGS.input_table
    if not FLAGS.output_partition:
        FLAGS.output_partition = FLAGS.input_partition + "_llm_infer"
    if not FLAGS.model_name:
        FLAGS.model_name = 'qwen/Qwen1.5-7B-Chat-AWQ'
    if FLAGS.infer_kernel not in InferFactory.factory_registry:
        logging.error(f'User deinfed kernel {FLAGS.infer_kernel} not be register')
    logging.info(f"flags: {json.dumps(FLAGS.flag_values_dict(), indent=4)}")


# default kernel
class SingleInfer:

    def compute(self, ctx):
        return ctx.llm(ctx.batch)

    def warm_up(self, llm):
        pass


class InferFactory:
    factory_registry = {
        'SingleInfer' : SingleInfer
    }

    @classmethod
    def register(cls, infer_class):
        cls.factory_registry[infer_class.__name__] = infer_class

    @classmethod
    def get_kernel(cls, name):
        return cls.factory_registry[name]


class InferContext:

    def __init__(self, llm, prompts, index=None):
        self.llm = llm
        self.prompts = prompts
        self.index = index


class OdpsHandle:

    def __init__(self, access_id, access_key, project, endpoint,
                 input_table, input_partition, columns,
                 output_table, output_partition, lifecycle=14,
                 batch_size=512, max_queue_len=1000):

        self.batch_size = batch_size
        self.max_queue_len = max_queue_len

        self.columns = columns.split(',')
        odps = ODPS(access_id, access_key, project, endpoint=endpoint)

        self.worker_num = int(os.environ.get("WORKER_SIZE", "1"))
        self.index = int(os.environ.get("RANK", "0"))

        if self.worker_num == 1:
            partition_spec = output_partition
        else:
            partition_spec = output_partition + "_" + str(self.index)
        try:
            self.table = odps.create_table(output_table, ('key string, value string', 'dt string'), lifecycle=lifecycle)
        except Exception as e:
            logging.fatal(e)
        self.table.create_partition(partition_spec, if_not_exists=True)
        upload_session = TableTunnel(odps).create_stream_upload_session(output_table, partition_spec=partition_spec)
        self.writer = upload_session.open_record_writer()

        download_session = TableTunnel(odps).create_download_session(input_table, partition_spec=input_partition)
        data_size = download_session.count//self.worker_num
        if data_size == 0:
            logging.error(f"Data size lower than woker num.")
        if self.index == self.worker_num-1:
            count = download_session.count - (self.worker_num-1)*data_size
        else:
            count = data_size
        start = self.index*data_size
        self.reader = download_session.open_record_reader(start, count, columns=self.columns)

        self.buffer = Queue(maxsize=self.max_queue_len)
        self.data_fetched = False
        self.fetch_thread = threading.Thread(target=self._fetch_data)
        self.fetch_thread.daemon = True
        self.fetch_thread.start()

        logging.info(f"Odps init info: {locals()}")

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.reader.close()
        self.writer.close()
        logging.info(f"Odps write done.")

    def _fetch_data(self):
        while True:
            try:
                data = self.reader.read()
                if not data:
                    self.data_fetched = True
                    logging.info(f"Fetch thread read done.")
                    break
                self.buffer.put(data, block=True)  # 如果队列满了就会阻塞
            except Exception as e:
                logging.info(f"Error fetching data: {e}")
                self.data_fetched = True
                break

    def batch(self):
        def process(batch):
            batch_index, batch_prompts = [], []
            if self.columns == 1:
                for item in batch:
                    batch_prompts.append(item[self.columns[-1]])
                return {"index": batch_prompts, "prompts": batch_prompts}
            else:
                for item in batch:
                    batch_index.append(item[self.columns[0]])
                    batch_prompts.append(item[self.columns[-1]])
                return {"index": batch_index, "prompts": batch_prompts}

        batch = []
        while len(batch) < self.batch_size:
            if self.data_fetched and self.buffer.empty():
                logging.info(f"Queue data completed.")
                break  # 如果数据获取完毕且缓冲区已空，则退出循环
            try:
                item = self.buffer.get(timeout=1.0)  # 使用超时来避免无限期阻塞
                batch.append(item)
                self.buffer.task_done()
            except Empty:
                # 在等待期间没有数据到达
                if self.data_fetched:
                    logging.info(f"Queue data completed.")
                    break
                continue  # 如果数据尚未获取完，则继续等待其他数据
        return process(batch)

    def write(self, batch_ins, batch_outs):
        for q, a in zip(batch_ins['index'], batch_outs):
            record = self.table.new_record()
            record['key'] = q
            record['value'] = a
            self.writer.write(record)


class LLMPredictor:

    def __init__(self, model_path,
                 enable_prefix_caching=False,
                 gpu_memory_utilization=0.9,
                 max_model_len=None,
                 max_tokens=None,
                 top_p=None,
                 top_k=None):
        tensor_parallel_size = int(os.environ.get("NPROC_PER_NODE", "1"))
        self.llm = LLM(model=model_path,
                       enable_prefix_caching=enable_prefix_caching,
                       gpu_memory_utilization=gpu_memory_utilization,
                       max_model_len=max_model_len,
                       tensor_parallel_size=tensor_parallel_size)

        self.sampling_params = SamplingParams(max_tokens=max_tokens,
                                              top_p=top_p,
                                              top_k=top_k,)

        logging.info("LLMPredictor init done!")

    def __call__(self, batch):
        outputs = self.llm.generate(batch, self.sampling_params)
        prompt = []
        generated_text = []
        for output in outputs:
            prompt.append(output.prompt)
            generated_text.append(' '.join([o.text for o in output.outputs]))
        return {
            "prompts": prompt,
            "generated_text": generated_text,
        }


class Executor:

    def __init__(self):

        check_config()

        model_dir = os.path.join('/modelset/model/', FLAGS.model_name.split('/')[-1].replace('.', '___'))
        if not os.path.exists(model_dir):
            model_dir = snapshot_download(FLAGS.model_name, cache_dir='/work')

        logging.info(f"Model path: {model_dir}")

        self.llm_predictor = LLMPredictor(model_dir,
                                          FLAGS.enable_prefix_caching,
                                          FLAGS.gpu_memory_utilization,
                                          FLAGS.max_model_len,
                                          FLAGS.max_tokens,
                                          FLAGS.top_p,
                                          FLAGS.top_k)

        self.kernel = InferFactory.get_kernel(FLAGS.infer_kernel)()

        logging.info(f"Executor kernel: {FLAGS.infer_kernel}")

    def run(self):

        if hasattr(self.kernel, 'warm_up'):
            logging.info(f"Warm Up: {json.dumps(self.kernel.warm_up(self.llm_predictor), indent=4, ensure_ascii=False)}")

        with OdpsHandle(FLAGS.access_id, FLAGS.access_key,
                        FLAGS.project, FLAGS.endpoint,
                        FLAGS.input_table, FLAGS.input_partition, FLAGS.columns,
                        FLAGS.output_table, FLAGS.output_partition, FLAGS.output_table_lifecycle,
                        FLAGS.batch_size, FLAGS.max_queue_len) as handle:
            counter = 0
            while True:
                batch = handle.batch()
                if batch['prompts']==[]: break
                outputs = self.kernel.compute(InferContext(self.llm_predictor, batch['prompts']))
                handle.write(batch, outputs['generated_text'])
                if counter % 1 == 0:
                    logging.info(f"Process batch: {counter}, size: {len(batch['prompts'])}")
                counter += 1


def infer_main(argv):
    Executor().run()


if __name__ == '__main__':
    logging.get_absl_handler().setLevel(logging.INFO)
    app.run(infer_main)
