import os

def extract_tasks(directory: str) -> list[dict]:
    tasks = []
    # 遍历目录的下一级子目录
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)
        if os.path.isdir(entry_path):
            readme_path = os.path.join(entry_path, "README.md")
            # 检查是否存在 README.md
            if os.path.exists(readme_path):
                # 读取 README.md 内容
                content = ""
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 收集子目录下的图片路径
                imgs = []
                for file in os.listdir(entry_path):
                    file_path = os.path.join(entry_path, file)
                    if os.path.isfile(file_path):
                        # 检查是否为图片文件（支持常见格式）
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                            imgs.append(file_path)
                
                # 构建 task 对象
                tasks.append({
                    "entry": entry,
                    "content": content,
                    "imgs": imgs
                })
    return tasks
