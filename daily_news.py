#!/usr/bin/env python3
"""
陈小蓝智能要闻助手
"""

import requests
import re
from datetime import datetime
from typing import List, Dict

# ============ 配置 ============
SENDKEY = "SCT345860T8LHiGPBoAKFb4u5qDDDELxyS"

NEWS_QUERIES = [
    {"category": "🤖 AI&前沿科技要闻", "queries": ["AI 人工智能 最新", "ChatGPT 大模型"]},
    {"category": "💹 金融要闻（美股纳斯达克）", "queries": ["纳斯达克 美股", "Apple Microsoft 股票"]},
    {"category": "🐢 龟鳖要闻", "queries": ["龟类养殖", "鳖类繁殖"]},
    {"category": "🧬 生物&野生动植物要闻", "queries": ["新物种发现", "生物科研"]},
    {"category": "🐍 爬虫水产行情要闻", "queries": ["爬宠市场", "水产养殖"]},
    {"category": "🌍 外交要闻", "queries": ["中国外交", "国际关系"]},
    {"category": "📰 国际大事要闻", "queries": ["国际新闻", "全球热点"]}
]
# ==============================


def send_wechat(title: str, content: str) -> bool:
    """发送微信"""
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    try:
        r = requests.post(url, data={"title": title, "desp": content}, timeout=30)
        if r.json().get("code") == 0:
            print("✅ 推送成功")
            return True
        print(f"❌ 失败: {r.json()}")
        return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False


def search_news(query: str) -> List[Dict]:
    """搜索新闻"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
        r = requests.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            pattern = r'<a class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, r.text)
            
            results = []
            for link, title in matches[:3]:
                t = re.sub(r'<[^>]+>', '', title).replace('&amp;', '&').strip()
                if t and len(t) > 5:
                    results.append({"title": t, "url": link})
            
            if results:
                print(f"  ✅ 找到 {len(results)} 条")
                return results
    except Exception as e:
        print(f"  ❌ 失败: {e}")
    return []


def main():
    print("🚀 启动新闻助手...")
    
    today = datetime.now().strftime("%Y年%m月%d日")
    content = f"# 📰 陈小蓝每日要闻\n\n**{today}**\n\n---\n"
    
    for cat in NEWS_QUERIES:
        content += f"\n## {cat['category']}\n\n"
        for q in cat["queries"]:
            print(f"📂 {q}")
            content += f"**【{q}】**\n"
            news = search_news(q)
            if news:
                for n in news:
                    content += f"- [{n['title']}]({n['url']})\n"
            else:
                content += "- 暂无消息\n"
        content += "\n"
    
    title = f"📰 陈小蓝每日要闻 | {datetime.now().strftime('%m月%d日')}"
    send_wechat(title, content)
    
    print("✅ 完成!")
    return 0


if __name__ == "__main__":
    exit(main())
