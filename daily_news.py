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
# Server酱 SendKey (从环境变量读取，GitHub Secrets中配置)
SENDKEY = "SCT345860T8LHiGPBoAKFb4u5qDDDELxyS"

# 新闻搜索关键词配置
NEWS_QUERIES = [
    {"category": "🤖 AI&前沿科技要闻", "queries": ["大模型动态 今日", "AI人工智能最新进展", "ChatGPT GPT最新消息"]},
    {"category": "💹 金融要闻（美股纳斯达克）", "queries": ["纳斯达克100 今日", "美股科技股 今日", "Apple Microsoft 股票"]},
    {"category": "🐢 龟鳖要闻", "queries": ["龟类养殖技术", "鳖类繁殖技术"]},
    {"category": "🧬 生物&野生动植物要闻", "queries": ["新物种发现", "生物科研突破"]},
    {"category": "🐍 爬虫水产行情要闻", "queries": ["爬宠市场 行情", "水产养殖 价格"]},
    {"category": "🌍 外交要闻", "queries": ["中国外交 最新动态", "国际关系 重大事件"]},
    {"category": "📰 国际大事要闻", "queries": ["国际重大新闻 今日", "全球热点事件"]}
]
# ==================================


def send_wechat(title: str, content: str) -> bool:
    """通过Server酱发送微信消息"""
    # 使用新版 Server酱 API
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    
    data = {
        "title": title,
        "desp": content
    }
    
    try:
        print(f"📤 正在推送至微信...")
        response = requests.post(url, data=data, timeout=30)
        
        # 打印原始响应，方便调试
        print(f"📬 Server酱响应状态码: {response.status_code}")
        print(f"📬 Server酱原始响应: {response.text[:200]}")
        
        # 尝试解析JSON
        try:
            result = response.json()
            print(f"📬 Server酱解析结果: {result}")
            
            # 新版API返回 code=0 表示成功
            if result.get("code") == 0 or result.get("errno") == 0:
                print(f"✅ 微信推送成功")
                return True
            else:
                print(f"❌ 推送失败: {result.get('message', result)}")
                return False
        except json.JSONDecodeError:
            # 如果不是JSON，检查是否返回 "success" 或 "ok"
            if "success" in response.text.lower() or "ok" in response.text.lower():
                print(f"✅ 微信推送成功")
                return True
            print(f"❌ Server酱返回非JSON格式")
            return False
            
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False


def search_news(query: str) -> List[Dict]:
    """搜索新闻"""
    search_url = "https://ddg-api.vercel.app/search"
    
    try:
        params = {"q": query, "region": "cn", "max_results": 2}
        response = requests.get(search_url, params=params, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            return [{"title": item.get("title", ""), "url": item.get("url", "")} for item in results[:2]]
    except Exception as e:
        print(f"  搜索失败 [{query}]: {e}")
    
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
            content += f"**【{query}】**\n"
            news = search_news(query)
            
            if news:
                for item in news:
                    content += f"- {item['title']}\n"
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
