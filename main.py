# 在本地创建项目
mkdir ai-daily-news
cd ai-daily-news

# 初始化Git
git init

# 复制所有配置文件到此目录
# 确保包含:.github/workflows/daily-update.yml, scripts/generate_report.py 等

# 提交到GitHub
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/ai-daily-news.git
git push -u origin main
