import logging
from colorama import init, Fore, Style
from tqdm import tqdm
from .path import root_path

# 初始化 colorama（自动转换 Windows 控制台代码）
init(autoreset=True)

# --- 设置 Logging ---
log_filename = root_path.joinpath("xblock.log")
logger = logging.getLogger("X_Blocker")
logger.setLevel(logging.INFO)

# 文件处理器 (写入文件)
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# 加入 logger
logger.addHandler(file_handler)


def log_message(message, level="info", color=None):
    """同步打印到日志文件与控制台，并加上颜色"""
    # 写入日志文件 (不含颜色代码)
    if level == "error":
        logger.error(message)
    else:
        logger.info(message)

    # 使用 tqdm.write 可以在打印日志时自动处理进度条的刷新，防止格式错乱
    formatted_msg = f"{color}{message}{Style.RESET_ALL}" if color else message
    tqdm.write(formatted_msg)
