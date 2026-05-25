import os, requests

corpid = os.environ.get("WECOM_CORP_ID", "未设置")
secret = os.environ.get("WECOM_AGENT_SECRET", "未设置")
agentid = os.environ.get("WECOM_AGENT_ID", "未设置")
touser = os.environ.get("WECOM_TO_USER", "未设置")

print(f"CORP_ID: [{corpid}]")
print(f"AGENT_ID: [{agentid}]")
print(f"TO_USER: [{touser}]")
print(f"SECRET 长度: {len(secret)}")
print()

# 测试获取 token
r = requests.get(
    f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}",
    timeout=10
)
print(f"token 接口返回: {r.text}")
