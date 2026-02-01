import requests
import time
import random
import os
import uuid
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# Slash Command 配置（从浏览器测试中获取）
APPLICATION_ID = "1444134513679532223"  # Core APP 的 Application ID
GUILD_ID = "1224401655689117787"        # HashGame Labs 服务器 ID
COMMAND_ID = "1455204006363140189"      # faucet 命令 ID
COMMAND_VERSION = "1455204006363140193" # faucet 命令版本

def get_config():
    """从环境变量读取配置"""
    token = os.getenv("DISCORD_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")
    wallet_address = os.getenv("WALLET_ADDRESS")
    session_id = os.getenv("SESSION_ID", str(uuid.uuid4().hex)[:32])
    
    if not token:
        raise ValueError("缺少 DISCORD_TOKEN，请在 .env 文件中配置")
    if not channel_id:
        raise ValueError("缺少 CHANNEL_ID，请在 .env 文件中配置")
    if not wallet_address:
        raise ValueError("缺少 WALLET_ADDRESS，请在 .env 文件中配置")
    
    return token, channel_id, wallet_address, session_id

def send_slash_command(token: str, channel_id: str, wallet_address: str, session_id: str) -> bool:
    """发送 /faucet Slash Command 到 Discord"""
    url = "https://discord.com/api/v9/interactions"
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    # Slash Command 的 Interactions API payload
    payload = {
        "type": 2,  # APPLICATION_COMMAND
        "application_id": APPLICATION_ID,
        "guild_id": GUILD_ID,
        "channel_id": channel_id,
        "session_id": session_id,
        "data": {
            "version": COMMAND_VERSION,
            "id": COMMAND_ID,
            "name": "faucet",
            "type": 1,
            "options": [
                {
                    "type": 3,  # STRING 类型
                    "name": "wallet_address",
                    "value": wallet_address
                }
            ]
        },
        "nonce": str(int(time.time() * 1000)) + str(random.randint(1000, 9999))
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # Interactions API 成功返回 204 No Content
        if response.status_code == 204:
            print(f"[成功] Slash Command 已发送: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        elif response.status_code == 200:
            print(f"[成功] Slash Command 已发送: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        elif response.status_code == 401:
            print("[失败] Token 无效或已过期，请更新 DISCORD_TOKEN")
            return False
        elif response.status_code == 403:
            print("[失败] 没有权限执行此命令")
            return False
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 60)
            print(f"[限流] 请求过于频繁，{retry_after} 秒后重试")
            time.sleep(retry_after)
            return False
        else:
            print(f"[失败] 状态码: {response.status_code}, 信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("[错误] 请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[错误] 网络请求失败: {e}")
        return False

def main():
    print("=" * 50)
    print("   Discord Faucet 自动领水脚本 (Slash Command)")
    print("=" * 50)
    print()
    
    try:
        token, channel_id, wallet_address, session_id = get_config()
    except ValueError as e:
        print(f"[配置错误] {e}")
        print("请复制 .env.example 为 .env 并填入你的配置")
        return
    
    print(f"频道 ID: {channel_id}")
    print(f"钱包地址: {wallet_address}")
    print("-" * 50)
    
    while True:
        send_slash_command(token, channel_id, wallet_address, session_id)
        
        # 等待 1 小时 + 随机延迟
        wait_time = 3600 + random.randint(10, 120)
        next_time = time.strftime('%H:%M:%S', time.localtime(time.time() + wait_time))
        print(f"下次执行时间: {next_time} (等待 {wait_time} 秒)")
        print()
        time.sleep(wait_time)

if __name__ == "__main__":
    main()