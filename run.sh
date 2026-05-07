#!/bin/bash
#
# KeyMouse Stats 启动脚本
#

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python依赖
echo "检查依赖..."
python3 -c "import PyQt5" 2>/dev/null || {
    echo "错误: PyQt5 未安装"
    echo "请运行: pip install -r requirements.txt"
    exit 1
}

python3 -c "import pynput" 2>/dev/null || {
    echo "错误: pynput 未安装"
    echo "请运行: pip install -r requirements.txt"
    exit 1
}

# 检查系统托盘支持
if ! qdbus org.kde.StatusNotifierWatcher /StatusNotifierWatcher org.kde.StatusNotifierWatcher.IsStatusNotifierHostRegistered &>/dev/null && \
   ! xprop -root _NET_SYSTEM_TRAY_S0 &>/dev/null; then
    echo "警告: 系统可能不支持系统托盘"
fi

# 启动应用
echo "启动 KeyMouse Stats..."
python3 main.py
