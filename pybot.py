import os
import re
import datetime
import json
import telebot
from git import Repo

# 静态博客项目仓库的绝对路径，默认自动识别为当前脚本所在目录
BLOG_REPO_PATH = os.path.dirname(os.path.abspath(__file__))

# ==================== 零依赖安全加载 .env 文件 ====================
env_path = os.path.join(BLOG_REPO_PATH, ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

# ==================== 配置区域 ====================
# 配置请在项目目录下的 .env 文件中进行 (格式：KEY=VALUE)

TG_TOKEN = os.environ.get("TG_TOKEN")

<<<<<<< HEAD
# 你的 Telegram User IDs (用于安全校验，支持多个，逗号分隔，只有受信任的用户能操作机器人)
# 你可以通过向机器人发送 /start 命令来获取你的 User ID
MY_TG_IDS_STR = os.environ.get("MY_TG_IDS", "")
TRUSTED_TG_IDS = [int(id.strip()) for id in MY_TG_IDS_STR.split(",") if id.strip().isdigit()]
=======
# 你的 Telegram User ID (用于安全校验，只有你自己能操作机器人)
# 你可以通过向机器人发送 /start 命令来获取你的 User ID
MY_TG_ID_STR = os.environ.get("MY_TG_ID")
MY_TG_ID = int(MY_TG_ID_STR) if (MY_TG_ID_STR and MY_TG_ID_STR.isdigit()) else None
>>>>>>> 9889973 (Optimize vertical spacing and add Kapibala reader link)

# 发布微博/碎碎念时的默认定位
DEFAULT_LOCATION = os.environ.get("DEFAULT_LOCATION", "南京")
# ==================================================

# 实例化机器人
bot = telebot.TeleBot(token=TG_TOKEN)

# 用于临时存储你正在写的主题，格式：{user_id: "当前主题"}
user_sessions = {}

# 提示词模板
PROMPT_TEMPLATE = """你现在是拥有百万粉丝的科技博主，文风干练有趣。请为写一条微博推广文案。

主题： {topic}

要求：

1. 字数严格限制在 60-75字 之间；

2. 结构：吸睛开头 + 核心价值 + 情绪化体验；

3. 语气：网感强、活泼、不说教，禁用“极致”“赋能”等互联网黑话；

4. 结尾自带 1个相关话题标签（如 #开源工具 #效率神器）。

输出： 仅输出文案正文，无需解释。"""


def insert_post_into_index_html(content, location=DEFAULT_LOCATION):
    """
    将 AI 生成的微博内容格式化后插入到 index.html 的 posts 数组的最前面
    """
    html_path = os.path.join(BLOG_REPO_PATH, "index.html")
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"找不到 index.html 文件: {html_path}")
        
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 生成 YYYY-MM-DD HH:MM 格式的日期时间
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 将内容格式化为标准的 JSON 字符串（处理好双引号、换行、反斜杠转义）
    escaped_content = json.dumps(content, ensure_ascii=False)
    
    # 构造待插入的 JS 对象行
    new_item = f'            {{ date: "{now_str}", location: "{location}", content: {escaped_content} }},'
    
    # 寻找 posts 数组的起点进行插入
    marker = "const posts = ["
    if marker in html_content:
        parts = html_content.split(marker, 1)
        updated_content = parts[0] + marker + "\n" + new_item + parts[1]
    else:
        # 兼容可能有空格或缩进差异的声明
        match = re.search(r'const\s+posts\s*=\s*\[', html_content)
        if match:
            matched_str = match.group(0)
            parts = html_content.split(matched_str, 1)
            updated_content = parts[0] + matched_str + "\n" + new_item + parts[1]
        else:
            raise ValueError("在 index.html 中无法定位到 'const posts = ['")
              
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    return now_str


# Help / Start 命令：显示配置状态并告知用户如何配置和获取 User ID
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    current_user_id = message.from_user.id
    welcome_text = (
        f"👋 **你好！我是你的静态微博/碎碎念发布助手。**\n\n"
        f"你的 Telegram User ID 是: `{current_user_id}`\n"
<<<<<<< HEAD
        f"请确保将其配置在 `pybot.py` 对应的 `.env` 文件中 `MY_TG_IDS` 字段里 (多个ID可用逗号分隔)，以解锁机器人操作权限。\n\n"
=======
        f"请确保将其配置在 `pybot.py` 的 `MY_TG_ID` 中，以解锁机器人操作权限。\n\n"
>>>>>>> 9889973 (Optimize vertical spacing and add Kapibala reader link)
        f"🚀 **使用步骤:**\n"
        f"1️⃣ 发送 `/new` 或 `/new <主题内容>` 开始创作。\n"
        f"2️⃣ 机器人会自动适配您的 AI 提示词模板并发送给您。\n"
        f"3️⃣ 请长按复制提示词发给其他 AI 生成文案。\n"
        f"4️⃣ 直接将 AI 生成的文案发送回机器人，机器人将自动更新 `index.html` 并提交部署！"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")


# 第一步：发送 /new 触发写微博流程
@bot.message_handler(commands=['new'])
def start_new_blog(message):
<<<<<<< HEAD
    if message.from_user.id not in TRUSTED_TG_IDS:
=======
    if message.from_user.id != MY_TG_ID:
>>>>>>> 9889973 (Optimize vertical spacing and add Kapibala reader link)
        print(f"⚠️ 拒绝未授权的用户访问: {message.from_user.id}")
        return
    
    # 尝试提取 /new 后带的主题参数
    args = message.text.split(None, 1)
    if len(args) > 1:
        topic = args[1].strip()
        generate_prompt_from_topic(message, topic)
    else:
        msg = bot.reply_to(message, "✍️ 请发送你要写的【微博主题】或【核心大纲】：")
        bot.register_next_step_handler(msg, receive_topic)


# 中转步骤：接收异步发送的主题
def receive_topic(message):
<<<<<<< HEAD
    if message.from_user.id not in TRUSTED_TG_IDS: 
=======
    if message.from_user.id != MY_TG_ID: 
>>>>>>> 9889973 (Optimize vertical spacing and add Kapibala reader link)
        return
    topic = message.text.strip() if message.text else ""
    if not topic:
        bot.reply_to(message, "❌ 主题不能为空，请发送 /new 重新开始")
        return
    generate_prompt_from_topic(message, topic)


# 第二步：生成适配过的提示词并发送给用户
def generate_prompt_from_topic(message, topic):
    # 保存当前用户的写作上下文主题
    user_sessions[message.from_user.id] = topic

    # 替换模板主题
    formatted_prompt = PROMPT_TEMPLATE.format(topic=topic)

    bot.reply_to(message, "📋 已为你适配并生成提示词！请长按复制下方代码框中的内容去调用其他 AI：")
    bot.send_message(message.chat.id, f"```\n{formatted_prompt}\n```", parse_mode="Markdown")
    
    msg = bot.send_message(message.chat.id, "🤖 请在 AI 生成后，将【生成好的微博文案】直接发回复我，我将为您自动完成静态网页更新与 Git 提交：")
    bot.register_next_step_handler(msg, handle_blog_content)


# 第三步：接收正文，自动更新 index.html 并提交发布
def handle_blog_content(message):
<<<<<<< HEAD
    if message.from_user.id not in TRUSTED_TG_IDS: 
=======
    if message.from_user.id != MY_TG_ID: 
>>>>>>> 9889973 (Optimize vertical spacing and add Kapibala reader link)
        return
    content = message.text.strip() if message.text else ""
    
    if not content:
        bot.reply_to(message, "❌ 接收到的内容为空，请重新发送 /new 开始！")
        return
    
    # 获取之前暂存的主题
    topic = user_sessions.get(message.from_user.id, "自动发布")
    
    bot.reply_to(message, "⏳ 正在更新代码并提交到 Git，请稍候...")

    try:
        # 1. 更新 index.html
        now_str = insert_post_into_index_html(content, location=DEFAULT_LOCATION)
        
        # 2. Git 自动化操作
        repo = Repo(BLOG_REPO_PATH)
        html_path = os.path.join(BLOG_REPO_PATH, "index.html")
        
        # 暂存 index.html
        repo.git.add(html_path)
        
        # 提交到本地仓库
        commit_msg = f"Feat: TG Bot 自动发布微博推广《{topic}》({now_str})"
        repo.index.commit(commit_msg)
        
        # 推送到远程 GitHub 仓库 (如果配置了 remote origin)
        remotes = [r.name for r in repo.remotes]
        if 'origin' in remotes:
            origin = repo.remote(name='origin')
            origin.push()
            push_msg = "成功推送到远程仓库"
        else:
            push_msg = "（未检测到名为 origin 的远程仓库，仅保存在本地 Commit）"

        # 清除 Session 上下文
        user_sessions.pop(message.from_user.id, None)
        
        bot.reply_to(
            message, 
            f"🎉 成功！微博内容已发布到 `index.html`。\n"
            f"📈 Git 提交信息: `{commit_msg}`\n"
            f"🚀 {push_msg}。\n"
            f"Cloudflare Pages 正在自动构建，约一分钟后即可更新！"
        )

    except Exception as e:
        bot.reply_to(message, f"❌ 自动化更新或发布失败，原因: {str(e)}")


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Telegram 微博/碎碎念助手已启动...")
    print(f"📂 仓库路径: {BLOG_REPO_PATH}")
    print(f"📍 默认定位: {DEFAULT_LOCATION}")
    
    if not TG_TOKEN:
        print("⚠️  严重警告: TG_TOKEN 未配置！请在 .env 文件中设置 TG_TOKEN")
    else:
        # 混淆打印 Token，符合核心安全 mandate: Never log, print, or commit secrets
        masked_token = TG_TOKEN[:10] + "..." + TG_TOKEN[-5:] if len(TG_TOKEN) > 15 else "***"
        print(f"✅ TG_TOKEN 已加载: {masked_token}")
        
<<<<<<< HEAD
    if not TRUSTED_TG_IDS:
        print("⚠️  警告: TRUSTED_TG_IDS 未配置！外部用户消息将被忽略。请向机器人发送 /start 获取你的 TG ID。")
    else:
        print(f"🔒 授权用户 IDs: {TRUSTED_TG_IDS}")
=======
    if MY_TG_ID is None:
        print("⚠️  警告: MY_TG_ID 未配置！外部用户消息将被忽略。请向机器人发送 /start 获取你的 TG ID。")
    else:
        print(f"🔒 授权用户 ID: {MY_TG_ID}")
>>>>>>> 9889973 (Optimize vertical spacing and add Kapibala reader link)
    print("=" * 50)
    
    # 启动轮询
    bot.infinity_polling()
