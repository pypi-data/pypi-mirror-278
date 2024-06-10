import os
import sys

def seed_everything(seed):
    import torch
    import numpy as np
    import random
    torch.manual_seed(seed)       # Current CPU
    torch.cuda.manual_seed(seed)  # Current GPU
    np.random.seed(seed)          # Numpy module
    random.seed(seed)             # Python random module
    torch.backends.cudnn.benchmark = False    # Close optimization
    torch.backends.cudnn.deterministic = True # Close optimization
    # torch.cuda.manual_seed_all(seed) # All GPU (Optional)

def set_process_gpu():
    import torch
    worker_id = int(os.environ.get('APP_WORKER_ID', 1))
    devices = os.environ.get('CUDA_VISIBLE_DEVICES', '')
 
    if not devices:
        print('current environment did not get CUDA_VISIBLE_DEVICES env ,so use the default')
        return torch.device("cpu")
    rand_max = 9527
    gpu_index = (worker_id + rand_max) % torch.cuda.device_count()
    res = f"pid: {os.getpid()}, worker_id: {worker_id} set gpu_id :{gpu_index}"
    torch.cuda.set_device(int(gpu_index))
    print(res)
    return torch.device(gpu_index)


def try_occupy_more_gpu_memory(max_mb, device):
    import torch
    N = 0
    L = []
    X = torch.zeros(250000, 1000)
    if max_mb < 1000:
        try:
            x = X.clone().to(device)
            del x
            print(f"预先使用{max_mb} MB gpu")
        except Exception as e:
            print(e)
    else:
        while N < max_mb:
            try:
                L.append(X.clone().to(device))
                N += 1000
            except Exception as e:
                print(e)
                for l in L:
                    del l
                break

        for l in L:
            del l
    print(f"N: {N} MB")