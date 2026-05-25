#!/usr/bin/env python3
"""陈小蓝每日要闻 - Server酱推送（奏章风格）"""
import requests, os, pathlib
from datetime import datetime

SENDKEY = os.environ.get("SENDKEY", "")

QUERIES = [
    ("🤖 AI&前沿科技", ["AI 人工智能", "ChatGPT 大模型"]),
    ("💹 金融（美股）", ["纳斯达克 美股", "Apple Microsoft 股票"]),
    ("🐢 龟鳖要闻", ["龟类养殖", "鳖类繁殖"]),
    ("🧬 生物&野生动植物", ["新物种发现", "生物科研"]),
    ("🐍 爬虫水产行情", ["爬宠市场", "水产养殖"]),
    ("🌍 外交要闻", ["中国外交", "国际关系"]),
    ("📰 国际大事", ["国际新闻", "全球热点"]),
]

def push(title: str, content: str) -> bool:
    try:
        r = requests.post(
            f"https://sctapi.ftqq.com/{SENDKEY}.send",
            data={"title": title, "desp": content},
            timeout=30
        )
        ok = r.json().get("code") == 0
        print(f"{'✅ 推送成功' if ok else f'❌ 失败: {r.json()}'}")
        return ok
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def news(query: str) -> list:
    import xml.etree.ElementTree as ET
    for attempt in range(3):
        try:
            r = requests.get(
                f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=zh-CN&gl=CN",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            items = []
            for item in ET.fromstring(r.content).findall('.//item')[:3]:
                t = item.findtext('title', '').replace('<b>','').replace('</b>','').strip()
                l = item.findtext('link', '')
                if t and len(t) > 5:
                    items.append(f"[{t}]({l})")
            if items:
                print(f"  ✅ {len(items)} 条")
                return items
            print(f"  ⚠️ 空结果，重试({attempt+1}/3)")
        except Exception as e:
            print(f"  ⚠️ 第{attempt+1}次: {e}")
        import time; time.sleep(2)
    return ["暂无消息"]

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    lock = pathlib.Path("/tmp/news.lock")
    if lock.exists() and lock.read_text().strip() == today:
        print("⏭️ 今天已发过，跳过")
        return 0

    today_cn = datetime.now().strftime('%Y年%m月%d日')
    lines = [
        f"## 臣 启禀吾主：\n",
        f"今日乃 {today_cn}，臣已为吾主汇总天下要闻，恭请御览。\n\n",
        f"---\n"
    ]
    for cat, qs in QUERIES:
        lines.append(f"\n### {cat}\n")
        for q in qs:
            print(f"📂 {q}")
            lines.append(f"\n**{q}**  \n")
            lines.extend(news(q))

    lines.append(f"\n---\n*臣 谨奏*")

    if push(f"【📰 吾主 陈小蓝 每日要闻已送达】", "\n".join(lines)):
        lock.write_text(today)
        print("✅ 完成！请在微信服务号查看")
        return 0
    return 1

if __name__ == "__main__":
    exit(main())
