import time
import browser_cookie3
from tqdm import tqdm
from utils.logger import log_message, Fore
from utils.helpers import load_config, load_ids_from_js, get_progress, save_progress
from core.blocker import block_user_automated


def main():
    # 读取配置
    config = load_config()
    config_settings = config.get("settings", {})
    config_request = config.get("request", {})

    limit_once_run = config_settings.get("limit_once_run", 10)

    rate_limit_interval = config_request.get("rate_limit_interval", 2)
    request_timeout = config_request.get("timeout", 5)

    log_message(
        f"已读取 API 请求配置： 请求间隔 {rate_limit_interval} s，超时时间 {request_timeout} s",
        "info",
        Fore.CYAN,
    )

    # 从浏览器获取 Cookie
    try:
        # 这里以 chromium 为例，你可以根据需要改为 .edge(), .firefox() 等
        cj = browser_cookie3.chromium(domain_name="x.com")
        log_message("读取浏览器 Cookie 成功！", "info", Fore.CYAN)
    except Exception as e:
        log_message(f"读取浏览器 Cookie 失败: {e}", "error", Fore.RED)
        exit()

    # 从 Cookie 中提取 ct0 (即 x-csrf-token)
    ct0_value = None
    for cookie in cj:
        if cookie.name == "ct0":
            ct0_value = cookie.value
            break

    if not ct0_value:
        log_message(
            "错误：未在 Cookie 中找到 'ct0' 字段。请确保你已在浏览器登录 X。",
            "error",
            Fore.RED,
        )
        exit()

    # 读取黑名单
    user_ids = load_ids_from_js()

    # 获取上次进度
    last_id = get_progress()
    start_index = 0

    if last_id and last_id in user_ids:
        start_index = user_ids.index(last_id) + 1
        log_message(f"从上次进度继续，用户：{last_id}", "info", Fore.CYAN)

    # 确定本次运行的实际数量（不超过 limit_once_run）
    remaining_ids = user_ids[start_index:]
    task_list = remaining_ids[:limit_once_run]

    log_message(
        f"剩余 {len(remaining_ids)} 个待屏蔽用戶，本次计划处理 {len(task_list)} 个。",
        "info",
        Fore.YELLOW,
    )

    # --- 简洁进度条 ---
    # ncols=80 控制宽度防止在小窗口换行
    pbar = tqdm(task_list, desc="正在批量屏蔽", unit="人", ncols=80)

    for uid in pbar:
        block_user_automated(uid, cj, ct0_value, request_timeout)

        # 每处理一个，就更新
        save_progress(uid)

        time.sleep(rate_limit_interval)

    log_message("本次批量操作已完成。", "info", Fore.CYAN)


if __name__ == "__main__":
    main()
