import requests
from utils.logger import log_message, Fore


def block_user_automated(target_user_id, cj, ct0_value, timeout=5):

    # 3. 配置请求参数
    url = "https://x.com/i/api/1.1/blocks/create.json"

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

    # 4. 发送请求
    try:
        response = requests.post(
            url, headers=headers, cookies=cj, data=data, timeout=timeout
        )

        if response.status_code == 200:
            log_message(f"屏蔽成功，用户: {target_user_id}", "info", Fore.GREEN)
        else:
            log_message(
                f"屏蔽失败，用户: {target_user_id}，失败响应: {response.text}",
                "error",
                Fore.RED,
            )

    except Exception as e:
        log_message(f"屏蔽失败，用户: {target_user_id}，原因：{e}", "error", Fore.RED)
