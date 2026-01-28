#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timedelta
import warnings

# 忽略SSL警告
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# ========== 配置区域 ==========
# 安全提醒：请在 GitHub Secrets 中配置名为 GEMINI_API_KEY 的变量
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
OUTPUT_FILE = "index.html"  # 改为 index.html 方便直接访问
DISABLE_SSL_VERIFY = True 

def generate_daily_brief():
    if not DEEPSEEK_API_KEY:
        print("❌ 错误: 未找到 API Key，请在 Secrets 中配置 DEEPSEEK_API_KEY")
        return

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    three_days_ago = (now - timedelta(days=3)).strftime("%Y-%m-%d")
    
    prompt = f"""
    你是一位顶级的UI/UX设计师和科技新闻编辑。请生成从 {three_days_ago} 到 {today_str} 的 AI 行业简报。

    ### 核心任务：
    1. 汇总过去 72 小时内的全球 AI 动态（重点关注：Apple, Google, OpenAI, NVIDIA 及中国头部厂商）。
    2. **链接可靠性**：必须为每条新闻提供真实的来源 URL。如果无法提供具体长链接，请链接至该媒体官网。
    3. **明文显示来源**：每个卡片底部必须标注 "来源：[媒体名称]"。

    ### 设计风格要求：
    - **背景**：纯白色 (#FFFFFF)；**字体**：Poppins (Google Fonts)。
    - **炫酷标题**：蓝色到紫色的渐变渐变效果。
    - **卡片设计**：白色卡片，圆角 16px，带有精致淡阴影。
    - **交互效果**：悬停时向上浮动并放大（transform: translateY(-5px) scale(1.01)），平滑过渡。
    - **链接**：整个卡片必须包裹在 <a> 标签内，点击新窗口打开。

    ### 内容板块：
    - 核心焦点 (3条)、技术动态 (6-8条)、商业市场 (4-6条)、战略启示 (3-5条)。
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat", # 或使用 deepseek-reasoner
        "messages": [
            {"role": "system", "content": "你是一位专注于极致视觉体验的代码生成器。请直接输出完整的 HTML 代码，包含 CSS 样式。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        print(f"🚀 正在生成 {today_str} 的炫酷简报...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=120,
            verify=not DISABLE_SSL_VERIFY
        )
        response.raise_for_status()
        html_content = response.json()['choices'][0]['message']['content']
        
        # 提取 HTML
        if '```html' in html_content:
            html_content = html_content.split('```html')[1].split('```')[0].strip()
        elif '```' in html_content:
            html_content = html_content.split('```')[1].split('```')[0].strip()
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 生成成功！文件名：{OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    generate_daily_brief()
