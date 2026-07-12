#!/bin/bash

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
  echo "请使用 sudo 或以 root 用户权限运行此脚本。"
  exit 1
fi

SERVICE_FILE="/etc/systemd/system/vibe-bot.service"
WORKDIR="/root/vibe-static-blog-by-mobile"
EXEC_PATH="/usr/bin/python3"
SCRIPT_PATH="$WORKDIR/pybot.py"

echo "正在创建 systemd 服务文件..."

cat <<EOF > $SERVICE_FILE
[Unit]
Description=Vibe Static Blog Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$WORKDIR
ExecStart=$EXEC_PATH $SCRIPT_PATH
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "正在加载并启动服务..."
systemctl daemon-reload
systemctl enable vibe-bot.service
systemctl restart vibe-bot.service

echo "服务已启动。请使用 'systemctl status vibe-bot.service' 查看状态。"
