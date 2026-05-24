#!/usr/bin/env python3
"""陈小蓝每日要闻 - 推送到企业微信（奏章风格）"""
import requests, os, pathlib
from datetime import datetime
from typing import Optional

WECOM_CORP_ID = os.environ.get("WECOM_CORP_ID", "")
WECOM_AGENT_SECRET = os.environ.get("WECOM_AGENT_SECRET", "")
WECOM_AGENT_ID = os.environ.get("WECOM_AGENT_ID", "")
WECOM_TO_USER = os.environ.get("WECOM_TO_USER", "")

QUERIES = [
    ("🤖 AI&前沿科技", ["AI 人工智能", "ChatGPT 大模型"]),
    ("💹 金融（美股）", ["纳斯达克 美股", "Apple Microsoft 股票"]),
    ("🐢 龟鳖要闻", ["龟类养殖", "鳖类繁殖"]),
    ("🧬 生物&野生动植物", ["新物种发现", "生物科研"]),
    ("🐍 爬虫水产行情", ["爬宠市场", "水产养殖"]),
    ("🌍 外交要闻", ["中国外交", "国际关系"]),
    ("📰 国际大事", ["国际新闻", "全球热点"]),
]

def get_token() -> Optional[str]:
    r = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={WECOM_CORP_ID}&corpsecret={WECOM_AGENT_SECRET}",
        timeout=10
    )
    d = r.json()
    return d.get("access_token") if d.get("errcode") == 0 else None

def push(text: str) -> bool:
    token = get_token()
    if not token:
        return False
    r = requests.post(
        f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
        json={"touser": WECOM_TO_USER, "msgtype": "markdown",
              "agentid": WECOM_AGENT_ID, "markdown": {"content": text},
              "enable_duplicate_check": 1, "duplicate_check_interval": 1800},
        timeout=15
    )
    return r.json().get("errcode") == 0

def news(query: str) -> list:
    import xml.etree.ElementTree as ET
    for _ in range(3):
        try:
            r = requests.get(
                f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=zh-CN&gl=CN",
                headers={"User-Agent": "Mozilla/5.0"}, timeout=15
            )
            items = []
            for item in ET.fromstring(r.content).findall('.//item')[:3]:
                t = (item.findtext('title','').replace('<b>','').replace('</b>','').strip())
                l = item.findtext('link','')
                if t and len(t)>5:
                    items.append(f"[{t}]({l})")
            if items:
                return items
        except:
            import time; time.sleep(2)
    return ["暂无消息"]

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    lock = pathlib.Path("/tmp/news.lock")
    if lock.exists() and lock.read_text().strip() == today:
        return 0

    today_cn = datetime.now().strftime('%Y年%m月%d日')
    lines = [
        f"**臣 启禀吾主：**\n",
        f"今日乃 {today_cn}，臣已为吾主汇总天下要闻，恭请御览。\n",
        f"{'═'*20}\n"
    ]
    for cat, qs in QUERIES:
        lines.append(f"\n── {cat} ──\n")
        for q in qs:
            lines.append(f"**{q}**")
            lines.extend(news(q))

    lines.append(f"\n{'═'*20}\n**臣 谨奏**")

    if push("\n".join(lines)):
        lock.write_text(today)
        print("✅ 手机查看企业微信")
        return 0
    return 1

if __name__ == "__main__":
    exit(main())
