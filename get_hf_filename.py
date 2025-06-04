import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://hf-mirror.com"
REPO = "stabilityai/stable-diffusion-2-1-base"
BRANCH = "main"

visited = set()

def get_full_url(path):
    return f"{BASE_URL}/{REPO}/tree/{BRANCH}/{path}".rstrip('/')

def get_files_recursive(path=""):
    url = get_full_url(path)
    if url in visited:
        return []
    visited.add(url)

    print(f"📂 正在访问: {url}")
    time.sleep(0.5)  # 限速，防止封禁

    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"⚠️ 访问失败: {url}，状态码 {res.status_code}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    files = []

    # 查找所有 <a href=...>
    for link in soup.find_all("a", href=True):
        href = link["href"]

        # 是文件
        if f"/blob/{BRANCH}/" in href:
            file_path = href.split(f"/blob/{BRANCH}/")[-1]
            files.append(file_path)

        # 是子目录
        elif f"/tree/{BRANCH}/" in href:
            folder_path = href.split(f"/tree/{BRANCH}/")[-1]
            if folder_path not in visited:
                files.extend(get_files_recursive(folder_path))

    return files

# 运行
all_files = get_files_recursive()
print("\n📜 仓库中所有文件路径：")
for f in sorted(set(all_files)):
    print(f)
