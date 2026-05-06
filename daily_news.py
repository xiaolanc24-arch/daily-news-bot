#!/usr/bin/env python3
"""
陈小蓝智能要闻助手 - 独立定时推送脚本
使用 Google News RSS 稳定获取新闻
"""

import requests
import feedparser
from datetime import datetime
from typing import List, Dict

# ============ 配置区域 ============
SENDKEY = "SCT345860T8LHiGPBoAKFb4u5qDDDELxyS"

NEWS_QUERIES = [
    {"category": "🤖 AI&前沿科技要闻", "queries": ["AI 人工智能", "大模型 ChatGPT"]},
    {"category": "💹 金融要闻（美股纳斯达克）", "queries": ["纳斯达克 美股", "Apple Microsoft 股票"]},
    {"category": "🐢 龟鳖要闻", "queries": ["龟类养殖", "鳖类繁殖"]},
    {"category": "🧬 生物&野生动植物要闻", "queries": ["新物种发现", "生物科研"]},
    {"category": "🐍 爬虫水产行情要闻", "queries": ["爬宠市场", "水产养殖"]},
    {"category": "🌍 外交要闻", "queries": ["中国外交", "国际关系"]},
    {"category": "📰 国际大事要闻", "queries": ["国际新闻", "全球热点"]}
]
# ==================================


def send_wechat(title: str, content: str) -> bool:
    """通过Server酱发送微信消息"""
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    data = {"title": title, "desp": content}
    
    try:
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        if result.get("code") == 0:
            print(f"✅ 微信推送成功")
            return True
        print(f"❌ 推送失败: {result}")
        return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False


def search_news(query: str) -> List[Dict]:
    """使用 Google News RSS 搜索新闻"""
    results = []
    
    try:
        # 使用 Google News RSS
        search_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                for entry in feed.entries[:3]:
                    title = entry.get('title', '')[:80]
                    link = entry.get('link', '')
                    # 清理标题中的 HTML
                    title = title.replace('<b>', '').replace('</b>', '')
                    if title and link:
                        results.append({"title": title, "url": link})
                
                print(f"  ✅ 找到 {len(results)} 条结果")
                return results
                
    except Exception as e:
        print(f"  ❌ RSS搜索失败: {e}")
    
    # 备用：使用 Bing News API
    try:
        api_url = "https://ddg-api.vercel.app/search"
        params = {"q": query, "region": "cn", "max_results": 2}
        resp = requests.get(api_url, params=params, timeout=10)
        if resp.status_code == 200:
            items = resp.json()
            return [{"title": item.get("title", ""), "url": item.get("url", "")} for item in items[:2]]
    except:
        pass
    
    return []


def generate_daily_news() -> str:
    """生成每日新闻简报"""
    print("🔍 开始抓取新闻...")
    
    today = datetime.now().strftime("%Y年%m月%d日")
    content = f"# 📰 陈小蓝每日要闻简报\n\n**📅 {today}**\n\n---\n"
    
    for category_info in NEWS_QUERIES:
        category = category_info["category"]
        content += f"\n## {category}\n\n"
        
        for query in category_info["queries"]:
            print(f"📂 正在获取: {query}")
            content += f"**【{query}】**\n"
            news = search_news(query)
            
            if news:
                for item in news:
                    content += f"- [{item['title']}]({item['url']})\n"
            else:
                content += f"- 暂无最新消息\n"
        content += "\n"
    
    return content


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 陈小蓝智能要闻助手 启动")
    print("=" * 50)
    
    news_content = generate_daily_news()
    title = f"📰 陈小蓝每日要闻 | {datetime.now().strftime('%m月%d日')}"
    
    success = send_wechat(title, news_content)
    
    print("\n" + "=" * 50)
    print("✅ 完成!" if success else "❌ 失败!")
    print("=" * 50)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
