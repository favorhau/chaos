import json
from pathlib import Path
from typing import Union, Dict, Any

def write_task_file(
    task_name: str,
    base_dir: Union[str, Path],
    data: Union[str, bytes, Dict[str, Any]],
    content_type: str,
    filename: str = None  # 新增参数，默认为None
) -> Path:
    """
    增强版任务文件写入工具（支持MD/图片/JSON），现在支持外部指定文件名
    
    参数:
    - task_name: 任务/项目标识
    - base_dir: 父级目录路径
    - data: 内容数据（支持字符串、字节流、字典）
    - content_type: 数据类型标识（md/image/json）
    - filename: 可选参数，自定义文件名
    """
    type_map = {
        "md": (str, "md内容必须是字符串"),
        "image": (bytes, "图片内容必须是字节流"),
        "json": (dict, "JSON数据必须是字典")
    }
    if content_type not in type_map:
        raise ValueError(f"无效类型: {content_type}，支持类型：{list(type_map.keys())}")
    
    data_type, type_error = type_map[content_type]
    if not isinstance(data, data_type):
        raise TypeError(type_error)

    base_path = Path(base_dir).expanduser().resolve()
    task_path = base_path / task_name
    task_path.mkdir(parents=True, exist_ok=True)
    
    # 如果未指定文件名，则根据不同类型设置默认值
    if not filename:
        if content_type == "md":
            filename = "README.md"
        elif content_type == "image":
            filename = "image.png"  # 默认图片格式可以根据实际情况调整
        else:  # JSON类型
            filename = "data.json"

    target = task_path / filename
    
    if content_type == "md":
        target.write_text(data, encoding="utf-8")
    elif content_type == "image":
        target.write_bytes(data)
    else:  # JSON类型
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return target