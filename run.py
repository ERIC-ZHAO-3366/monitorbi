import requests
import os

# 从环境变量中获取机密
WEBHOOK_URL = os.environ['WEBHOOK_URL']
UID = os.environ['UID']
EXPECTED_NAME = os.environ['EXPECTED_NAME']
# B站API URL，用于获取用户信息
BILI_API_URL = "https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp"

def check_bili_username(uid, expected_name):
    # 自定义请求头，包括User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }
    # 使用B站API获取用户信息，包含自定义的请求头
    response = requests.get(BILI_API_URL.format(uid=uid), headers=headers)
    if response.status_code == 200:
        data = response.json()
        name = data.get("data", {}).get("name", "")
        # 检查名称是否匹配
        if name != expected_name:
            # 如果不匹配，发送Webhook通知
            payload = {"msgtype":"text","text": {"content":f"B站账户名称不匹配：期望的是'{expected_name}'，但获取到的是'{name}'。"}}
            webhook_response = requests.post(WEBHOOK_URL, json=payload, headers=headers)  # 同样为Webhook请求设置User-Agent
            print("已发送Webhook通知。")
            print(f"Webhook返回状态码: {webhook_response.status_code}")
            print(f"Webhook返回内容: {webhook_response.text}")
        else:
            payload = {"msgtype":"text","text": {"content":f"B站账户名称匹配：获取的是'{name}'。"}}
            webhook_response = requests.post(WEBHOOK_URL, json=payload, headers=headers) 
            print("B站账户名称匹配。")
            print(f"Webhook返回状态码: {webhook_response.status_code}")
            print(f"Webhook返回内容: {webhook_response.text}")
    else:
        print(response.status_code)
        print("获取B站用户信息失败。")

# 调用函数
check_bili_username(UID, EXPECTED_NAME)
