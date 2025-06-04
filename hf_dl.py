import os
import requests

base_url = "https://hf-mirror.com/stabilityai/stable-diffusion-2-1-base/resolve/main"
target_dir = "./models/stable-diffusion-2-1-base"

files_to_download = [
    "model_index.json",
    "vae/config.json",
    "vae/diffusion_pytorch_model.bin",
    "unet/config.json",
    "unet/diffusion_pytorch_model.bin",
    "scheduler/scheduler_config.json",
    "tokenizer/tokenizer_config.json",
    "tokenizer/vocab.json",
    "tokenizer/merges.txt",
    "text_encoder/config.json",
    "text_encoder/model.safetensors",
    "text_encoder/pytorch_model.bin",  # 有些模型使用 bin 文件
    "feature_extractor/preprocessor_config.json"
]

os.makedirs(target_dir, exist_ok=True)

for f in files_to_download:
    url = f"{base_url}/{f}"
    local_path = os.path.join(target_dir, f)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    print(f"⬇️ Downloading {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as out:
            for chunk in r.iter_content(chunk_size=8192):
                out.write(chunk)
print("✅ 所有文件下载完成")
