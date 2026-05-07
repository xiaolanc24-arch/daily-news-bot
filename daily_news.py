#!/usr/bin/env python3
"""
陈小蓝智能要闻助手 - 使用 NewsAPI 稳定版
"""

import requests
import json
from datetime import datetime
from typing import List, Dict

# ============ 配置 ============
SENDKEY = "SCT345860T8LHiGPBoAKFb4u5qDDDELxyS"

NEWS_QUERIES = [
    {"category": "🤖 AI&前沿科技要闻", "queries": ["AI 人工智能", "ChatGPT 大模型"]},
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
    """使用 NewsData.io 免费 API 搜索"""
    results = []
    
    # 方法1: NewsData.io API (免费额度)
    try:
        # 你需要去 https://newsdata.io 免费申请一个 API key
        # 暂时用备用方式
        pass
    except:
        pass
    
    # 方法2: 使用 Google News RSS (最稳定)
    try:
        import xml.etree.ElementTree as ET
        
        search_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        r = requests.get(search_url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            
            for item in root.findall('.//item')[:3]:
                title = item.find('title')
                link = item.find('link')
                
                if title is not None and link is not None:
                    t = title.text or ""
                    l = link.text or ""
                    
                    # 清理标题中的 HTML
                    t = t.replace('<b>', '').replace('</b>', '')
                    t = t.strip()
                    
                    if t and len(t) > 5:
                        results.append({"title": t, "url": l})
            
            if results:
                print(f"  ✅ 找到 {len(results)} 条")
                return results
                
    except Exception as e:
        print(f"  ❌ RSS失败: {e}")
    
    # 方法3: 备用 API
    try:
        api_url = "https://api.currentsapi.services/api/v1/latest_news"
        params = {
            "apiKey": "demo",  # 需要申请真实key
            "keywords": query,
            "language": "zh"
        }
        r = requests.get(api_url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            news = data.get("news", [])
            for n in news[:3]:
                results.append({
                    "title": n.get("title", "")[:80],
                    "url": n.get("url", "")
                })
            if results:
                print(f"  ✅ 备用API找到 {len(results)} 条")
                return results
    except:
        pass
    
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
