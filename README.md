# 🤖 Vibe Static Blog Bot Framework

这是一个极简、全自动化的 **"Telegram 驱动的静态网站 CMS"** 框架。

它通过 Telegram 机器人连接您的静态博客仓库。您可以直接在手机上通过 Telegram 发送主题，AI 辅助生成文案，机器人自动更新您的静态代码并提交 Git，触发 Cloudflare Pages 或 GitHub Pages 自动部署。

---

## 🏗 工作原理
```text
[Telegram 用户] --(发送内容)--> [Telegram Bot] --(更新 index.html)--> [Git Commit & Push]
                                                                             |
                                                                             v
[Cloudflare / GitHub Pages] <--(监测到 Git 变动，自动构建) <------------------+
```

---

## 🚀 快速上手 (Fork/Clone 本仓库)

### 1. 准备工作
- 拥有一个静态网站（如 HTML, Hugo, Hexo 站点）。
- 确保网站仓库支持 Git 提交。
- 拥有一台 VPS（用于长期运行 Python 机器人）。

### 2. 环境配置
在 VPS 上安装 Python 3 环境：

```bash
sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install pyTelegramBotAPI GitPython
```

### 3. 设置您的 Telegram Bot
1. 在 Telegram 搜索 [@BotFather](https://t.me/BotFather)，发送 `/newbot` 创建机器人，获取 **Token**。
2. 将此仓库 Clone 到您的 VPS。

### 4. 初始化（清理演示数据）
因为仓库包含了演示用的历史文章数据，在开始使用前，请运行以下命令一键清空：

```bash
python3 reset_blog.py
```
*(该操作会清空 index.html 中的历史文章列表，请确认后操作)*

### 5. 配置环境
创建 `.env` 文件（不要上传此文件！）：
   ```bash
   # 项目目录下的 .env
   TG_TOKEN=您的_BOT_TOKEN
   MY_TG_ID=您的_TELEGRAM_USER_ID
   DEFAULT_LOCATION=您的城市
   ```
   *注意：若不知道 `MY_TG_ID`，启动机器人后，使用您的账号发送 `/start`，机器人回复中会显示该 ID。*

### 6. 适配您的网站
由于每个静态网站的 HTML 结构不同，您需要修改 `pybot.py` 中的 `insert_post_into_index_html` 函数，以适配您的 `index.html` 或对应文章列表文件的 JSON/JS 插入逻辑。

### 7. 启动与后台运行
在仓库目录下直接运行测试：
```bash
python3 pybot.py
```

**长期后台运行 (systemd):**
创建 `/etc/systemd/system/tg-blog-bot.service`:
```ini
[Unit]
Description=Telegram Blog Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/your/repo
ExecStart=/usr/bin/python3 /path/to/your/repo/pybot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
然后执行 `systemctl enable --now tg-blog-bot` 即可。

---

## 📝 框架核心组件
- `pybot.py`: 机器人主逻辑，负责指令交互、适配 AI 提示词、HTML 自动化更新、Git 操作。
- `.env`: 环境变量配置 (请加入 `.gitignore` 保护隐私)。
- `test_pybot.py`: 单元测试，确保您的 HTML 更新逻辑不会破坏代码结构。

## 💡 提示
- 您可以修改 `pybot.py` 中的 `PROMPT_TEMPLATE` 变量，定制属于您的 AI 写作风格。
- 机器人发布后，网页更新通常取决于您的 Pages 构建时间（通常约 1 分钟）。
