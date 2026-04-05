import requests
import time
from utils.logger import log_message, Fore


def make_req_data(target_user_id, ct0_value):
    headers = {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/x-www-form-urlencoded",
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "zh-tw",
        # 关键步骤：动态同步 csrf 令牌
        "x-csrf-token": ct0_value,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    data = {"user_id": target_user_id}

    return headers, data


def send_block_req(
    target_user_id,
    url,
    headers,
    cj,
    data,
    timeout=5,
    req_times_left=3,
    retry_interval=5,
):

    if req_times_left <= 0:
        return

    try:
        response = requests.post(
            url, headers=headers, cookies=cj, data=data, timeout=timeout
        )

        if response.status_code == 200:
            log_message(f"屏蔽成功，用户: {target_user_id}", "info", Fore.GREEN)
        elif response.json()["errors"][0]["code"] == 50:
            # 响应为 {"errors":[{"code":50,"message":"User not found."}]} 也视为成功
            log_message(f"屏蔽无效，用户: {target_user_id} 不存在", "info", Fore.GREEN)
        else:
            if req_times_left == 1:
                log_message(
                    f"屏蔽失败，用户: {target_user_id} ，失败响应: {response.text}",
                    "error",
                    Fore.RED,
                )
            else:
                time.sleep(retry_interval)

            send_block_req(
                target_user_id,
                url,
                headers,
                cj,
                data,
                timeout,
                req_times_left - 1,
                retry_interval,
            )

    except Exception as e:
        if req_times_left == 1:
            log_message(
                f"屏蔽异常，用户: {target_user_id} ，原因：{e}", "error", Fore.RED
            )
        else:
            time.sleep(retry_interval)

            send_block_req(
                target_user_id,
                url,
                headers,
                cj,
                data,
                timeout,
                req_times_left - 1,
                retry_interval,
            )


def block_user_automated(
    target_user_id, cj, ct0_value, timeout=5, retry_times=3, retry_interval=5
):

    url = "https://x.com/i/api/1.1/blocks/create.json"

    headers, data = make_req_data(target_user_id, ct0_value)

    send_block_req(
        target_user_id, url, headers, cj, data, timeout, retry_times, retry_interval
    )
