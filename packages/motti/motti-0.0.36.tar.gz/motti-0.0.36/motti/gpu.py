import os
import logging
import time

def init_logger(
        logdir: str="log",
        logname: str="root"
    ) -> logging.Logger:
        logger = logging.getLogger(logname)
        logger.setLevel(logging.DEBUG)

        os.makedirs(logdir, exist_ok=True)
        # filename = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())) + ".log"
        filename = os.uname()[1] + "_" + time.strftime("%Y%m%d", time.localtime(time.time())) + ".log"
        log_path = os.path.join(logdir, filename)

        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - " \
            "%(process)d - " \
            "%(name)s - " \
            "%(levelname)s - " \
            "%(message)s"
        )

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

def get_the_most_idle_gpu_index_and_free_memory():
    import pynvml
    pynvml.nvmlInit()  # 初始化

    def f(threshold=8000):
        gpu_device_count = pynvml.nvmlDeviceGetCount()  # 获取Nvidia GPU块数

        return_gpu_index = 0
        max_free_memory = -1

        for gpu_index in range(gpu_device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)  # 获取GPU i的handle，后续通过handle来处理
            memery_info = pynvml.nvmlDeviceGetMemoryInfo(handle)  # 通过handle获取GPU 的信息
            if memery_info.free > max_free_memory:
                max_free_memory = memery_info.free
                return_gpu_index = gpu_index

        if (max_free_memory>>20) > threshold:
            return return_gpu_index
        else:
            return -1
    return f


def set_process_gpu():
    import torch
    worker_id = int(os.environ.get('APP_WORKER_ID', 1))
    devices = os.environ.get('CUDA_VISIBLE_DEVICES', '')
 
    if not devices:
        print('current environment did not get CUDA_VISIBLE_DEVICES env ,so use the default')
        return 0

    rand_max = 9527
    gpu_index = (worker_id + rand_max) % torch.cuda.device_count()
    torch.cuda.set_device(int(gpu_index))
    res = f"pid: {os.getpid()}, worker_id: {worker_id} set gpu_id :{gpu_index}"
    print(res)
    return gpu_index
