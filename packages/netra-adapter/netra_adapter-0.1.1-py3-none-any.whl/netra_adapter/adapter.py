# netra_adapter/adapter.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .utils import load_lora_weights

class LoRAAdapterManager:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to('cuda')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.lora_weights = {}
        self.hooks = {}

    def load_lora_weights(self, adapter_name, filepath):
        self.lora_weights[adapter_name] = load_lora_weights(filepath)

    def integrate_lora_weights(self, adapter_name):
        if adapter_name not in self.lora_weights:
            raise ValueError(f"Adapter {adapter_name} not found. Please load the adapter weights first.")
        
        hooks = []
        for name, param in self.model.named_parameters():
            if name in self.lora_weights[adapter_name]:
                hook = param.register_hook(lambda grad, lw=self.lora_weights[adapter_name][name]: grad + lw.data)
                hooks.append(hook)
        self.hooks[adapter_name] = hooks
        print(f'Setup: {adapter_name} LoRA adapter')

    def remove_adapter_hooks(self, adapter_name):
        if adapter_name in self.hooks:
            for hook in self.hooks[adapter_name]:
                hook.remove()
            del self.hooks[adapter_name]
            print(f'Unplugged: {adapter_name} LoRA adapter')

    def remove_all_hooks(self):
        for adapter_name, hooks in self.hooks.items():
            for hook in hooks:
                hook.remove()
        self.hooks = {}
        print('Unplugged: All LoRA adapters')

    def generate_response(self, query, max_length=50):
        inputs = self.tokenizer(query, return_tensors="pt").to('cuda')
        outputs = self.model.generate(**inputs, max_length=max_length)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
