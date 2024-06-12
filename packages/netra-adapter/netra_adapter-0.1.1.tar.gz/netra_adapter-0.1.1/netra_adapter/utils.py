# netra_adapter/utils.py

import torch
import psutil

def load_lora_weights(filepath):
    return torch.load(filepath, map_location='cuda')

def get_memory_usage():
    # Get CPU RAM usage
    cpu_memory = psutil.virtual_memory().used
    # Get GPU VRAM usage
    vram_memory = torch.cuda.memory_allocated()
    return cpu_memory, vram_memory
