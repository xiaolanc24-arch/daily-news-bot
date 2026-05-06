#!/usr/bin/env python3
"""
陈小蓝智能要闻助手 - 独立定时推送脚本
每天自动抓取新闻并通过Server酱推送到微信
"""

import requests
import json
from datetime import datetime
from typing import List, Dict

# ============ 配置区域 ============
# Server酱 SendKey
SENDKEY = "SCT345860T8LHiGPBoAKFb4u5qDDDELxyS"

# 新闻搜索关键词配置
NEWS_QUERIES = [
    {
        "category": "🤖 AI&前沿科技要闻",
        "queries": [
            "大模型动态 今日",
            "AI人工智能最新进展",
            "ChatGPT GPT最新消息",
            "英伟达 AI芯片 动态"
        ]
    },
    {
        "category": "💹 金融要闻（美股纳斯达克）",
        "queries": [
            "纳斯达克100 今日行情",
            "美股 科技股 今日",
            "标普500 今日收盘",
            "Apple Microsoft Google 股票"
        ]
    },
    {
        "category": "🐢 龟鳖要闻",
        "queries": [
            "龟类养殖技术 最新",
            "鳖类繁殖技术 突破",
            "龟鳖市场行情"
        ]
    },
    {
        "category": "🧬 生物&野生动植物要闻",
        "queries": [
            "新物种发现 最新",
            "生物科研突破 今日",
            "野生动植物保护"
        ]
    },
    {
        "category": "🐍 爬虫水产行情要闻",
        "queries": [
            "爬宠市场 今日行情",
            "水产养殖 价格 动态",
            "观赏鱼 热门品种"
        ]
    },
    {
        "category": "🌍 外交要闻",
        "queries": [
            "中国外交 最新动态",
            "国际关系 重大事件",
            "G20 外交 今日"
        ]
    },
    {
        "category": "📰 国际大事要闻",
        "queries": [
            "国际重大新闻 今日",
            "全球热点事件",
            "俄乌冲突 最新进展",
            "中东局势 最新"
        ]
    }
]
# ==================================


def send_wechat(title: str, content: str) -> bool:
    """通过Server酱发送微信消息"""
    url = f"https://sct.ftqq.com/{SENDKEY}.send"
    
    data = {
        "title": title,
        "desp": content
    }
    
    try:
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        
        if result.get("code") == 0 or result.get("errno") == 0:
            print(f"✅ 微信推送成功")
            return True
        else:
            print(f"❌ 推送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False


def search_news(query: str) -> List[Dict]:
    """搜索新闻"""
    search_url = "https://ddg-api.vercel.app/search"
    
    try:
        params = {
            "q": query,
            "region": "cn",
            "max_results": 3
        }
        response = requests.get(search_url, params=params, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            news_items = []
            for item in results[:3]:
                news_items.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", "")[:100]
                })
            return news_items
    except Exception as e:
        print(f"搜索失败 [{query}]: {e}")
    
    return []


def format_news_section(category: str, queries: List[str]) -> str:
    """格式化单个新闻板块"""
    section = f"\n## {category}\n\n"
    
    for query in queries:
        section += f"**【{query}】**\n"
        news = search_news(query)
        
        if news:
            for i, item in enumerate(news, 1):
                section += f"- {item['title']}\n"
                if item.get('snippet'):
                    section += f"  {item['snippet']}...\n"
        else:
            section += f"- 暂无最新消息\n"
        section += "\n"
    
    return section


def generate_daily_news() -> str:
    """生成每日新闻简报"""
    print("🔍 开始抓取新闻...")
    
    today = datetime.now().strftime("%Y年%m月%d日 %A")
    
    content = f"""
# 📰 陈小蓝每日要闻简报

**📅 {today}**

---
"""
    
    for category_info in NEWS_QUERIES:
        category = category_info["category"]
        queries = category_info["queries"]
        
        print(f"📂 正在获取: {category}")
        content += format_news_section(category, queries)
        content += "---\n"
    
    content += f"""
---
📌 **说明**: 本简报由陈小蓝专属助理自动生成
🕘 生成时间: {datetime.now().strftime("%H:%M:%S")}
"""
    
    return content


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 陈小蓝智能要闻助手 启动")
    print("=" * 50)
    
    # 生成新闻
    news_content = generate_daily_news()
    
    # 发送微信
    title = f"📰 陈小蓝每日要闻 | {datetime.now().strftime('%m月%d日')}"
    
    print("\n📤 正在发送微信推送...")
    success = send_wechat(title, news_content)
    
    if success:
        print("\n✅ 今日新闻推送完成！")
    else:
        print("\n❌ 推送失败，请检查Server酱配置")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
