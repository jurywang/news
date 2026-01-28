#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# ========== 配置区域 ==========
DEEPSEEK_API_KEY = "sk"
OUTPUT_FILE = "ai_brief_today.html"
DISABLE_SSL_VERIFY = True


def generate_daily_brief():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    three_days_ago = (now - timedelta(days=3)).strftime("%Y-%m-%d")

    # 核心改进：极其严厉的链接与来源指令，并强调新的设计风格
    prompt = f"""
    你是一位顶级的UI/UX设计师和科技新闻编辑，擅长用极具现代感的白色背景设计风格来呈现信息。请生成从 {three_days_ago} 到 {today_str} 的 AI 行业简报。

    ### 核心任务：
    1. 汇总过去 72 小时内的全球 AI 动态。
    2. **链接可靠性（核心）：** 必须为每条新闻提供真实的来源。如果无法提供该文章的具体 URL，请直接提供该新闻媒体的官方域名（例如：https://36kr.com 或 https://www.theverge.com）。
    3. **明文显示来源：** 每个卡片底部必须有一行文字： "来源：[媒体名称]"。

    ### HTML 结构和**设计风格要求（全新）**：
    - **整体背景**：纯白色背景 (#FFFFFF)。
    - **主要字体**：引入 Google Fonts 的 `Poppins` (用于标题和主要内容) 和 `Roboto Mono` (用于代码或特殊强调)。确保字体适配，大小适中。
    - **颜色方案**：以白色为主，搭配 #333333 (深灰文本)、#666666 (次要文本)、#007BFF (科技蓝) 和 #6F42C1 (紫色渐变)。
    - **炫酷标题**：主标题使用 `linear-gradient` 渐变色 (`#007BFF` 到 `#6F42C1`)，字体粗大，具有视觉冲击力。
    - **卡片设计**：
        - 纯白背景，圆角(16px)。
        - 边框：`1px solid #E0E0E0` (柔和灰色)。
        - 阴影：`box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);` (精致、轻微的阴影)。
        - **交互动画**：悬停时，`transform: translateY(-5px) scale(1.01);` (轻微上浮并放大)，`box-shadow` 增强，`transition: all 0.3s ease-out;` (平滑过渡)。
        - 每条新闻卡片必须是 `<a>` 标签包裹，`target="_blank"`。
    - **信息层级**：使用 `margin`, `padding` 和 `font-weight` 明确区分标题、摘要和来源。
    - **排版**：内容居中，最大宽度限制，提供舒适的阅读体验。
    - **底部来源**：在卡片内部右下角，使用 `#007BFF` 颜色的文字标出：“点击跳转至 [具体媒体名] ➔”。

    ### 内容板块：
    - 核心焦点 (3条)
    - 技术动态 (6-8条)
    - 商业市场 (4-6条)
    - 战略启示 (3-5条)
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system",
             "content": "你是一位顶级设计师和新闻编辑。请严格按照要求，输出美观且功能完备的白色背景HTML代码，确保所有链接可靠且来源明确。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  # 降低随机性，确保风格和链接的稳定
        "max_tokens": 8000
    }

    try:
        print(f"🚀 正在生成炫酷白色风格的 AI 简报（涵盖 {three_days_ago} 至 {today_str}）...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=120,
            verify=not DISABLE_SSL_VERIFY
        )
        response.raise_for_status()
        html_content = response.json()['choices'][0]['message']['content']

        # 提取 HTML 块
        if '```html' in html_content:
            html_content = html_content.split('```html')[1].split('```')[0].strip()

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ 炫酷简报生成成功！文件保存在: {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ 运行出错: {e}")


if __name__ == "__main__":
    generate_daily_brief()
