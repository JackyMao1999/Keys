#!/bin/bash
#
# KeyMouse Stats 安装脚本
#

set -e

echo "=== KeyMouse Stats 安装脚本 ==="
echo

# 检查Python版本
python3 --version || {
    echo "错误: Python3 未安装"
    exit 1
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 创建配置目录
CONFIG_DIR="$HOME/.config/keymouse-stats"
mkdir -p "$CONFIG_DIR"
echo "✓ 配置目录: $CONFIG_DIR"

# 安装Python依赖
echo
echo "安装Python依赖..."
pip install -r requirements.txt --user

# 检查Qt库
echo
echo "检查Qt库..."
if dpkg -l | grep -q python3-pyqt5; then
    echo "✓ PyQt5 已安装"
else
    echo "提示: 可选安装系统Qt库 (Ubuntu/Debian):"
    echo "      sudo apt-get install python3-pyqt5 libxcb-xinerama0"
fi

# 创建快捷方式 (可选)
DESKTOP_FILE="$HOME/.local/share/applications/keymouse-stats.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    echo "✓ 快捷方式已存在"
else
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=KeyMouse Stats
Comment=键盘鼠标使用统计
Exec=$SCRIPT_DIR/main.py
Icon=computer
Terminal=false
Type=Application
Categories=Utility;System;
EOF
    echo "✓ 快捷方式已创建: $DESKTOP_FILE"
fi

# 设置启动脚本权限
chmod +x "$SCRIPT_DIR/run.sh"
chmod +x "$SCRIPT_DIR/main.py"

echo
echo "=== 安装完成 ==="
echo
echo "运行方式:"
echo "  1. $SCRIPT_DIR/run.sh"
echo "  2. 或直接运行: python3 $SCRIPT_DIR/main.py"
echo
