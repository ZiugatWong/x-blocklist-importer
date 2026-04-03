import json
import os
import yaml
from .logger import log_message, Fore
from .path import root_path


def load_config():
    """读取 YAML"""
    try:
        with open(
            root_path.joinpath("config", "config.yaml"), "r", encoding="utf-8"
        ) as f:
            config = yaml.safe_load(f)
            return config
    except Exception as e:
        log_message(f"读取配置 YAML 失败！: {e}", "error", Fore.RED)
        return {}


def get_progress():
    """读取上次处理过的最后 ID"""
    progress_file_resolve_path = root_path.joinpath("progress.txt")
    if os.path.exists(progress_file_resolve_path):
        with open(progress_file_resolve_path, "r") as f:
            return f.read().strip()
    return None


def save_progress(user_id):
    """储存当前处理成功的 ID"""
    with open(root_path.joinpath("progress.txt"), "w") as f:
        f.write(str(user_id))


def load_ids_from_js():
    """从 block.js 中提取所有 accountId"""
    try:
        with open(root_path.joinpath("data", "block.js"), "r", encoding="utf-8") as f:
            content = f.read()
            # 去掉 window.YTD.block.part0 =
            json_str = content.split("=", 1)[1].strip()
            # 解析 JSON
            data = json.loads(json_str)
            # 提取 accountId 列表
            return [item["blocking"]["accountId"] for item in data]
    except Exception as e:
        log_message(f"读文件失败: {e}", "error", Fore.RED)
        return []
