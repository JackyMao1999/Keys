# KeyMouse Stats

一款简洁的Linux键盘鼠标使用统计后台应用，在系统托盘显示实时统计数据。

## 功能特性

- **键盘敲击统计** - 实时统计每日键盘按键次数
- **鼠标点击统计** - 分别统计左键和右键点击次数
- **鼠标移动距离** - 追踪鼠标移动的总像素距离
- **滚动距离统计** - 记录页面滚动的累计距离
- **菜单栏显示** - 核心数据直接显示在系统托盘
- **详细面板** - 点击托盘图标查看完整统计信息
- **每日自动重置** - 午夜自动重置统计数据
- **数据持久化** - 应用重启后数据不丢失

## 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 确保系统安装了Qt5相关库 (Ubuntu/Debian)
sudo apt-get install python3-pyqt5 libxcb-xinerama0

# 或 (Fedora)
sudo dnf install python3-pyqt5
```

## 运行方式

```bash
# 直接运行
python3 main.py

# 强制命令行模式
python3 main.py --cli

# 强制 GUI 模式（托盘 + 后台统计）
python3 main.py --gui

# 仅打开 GUI 详情面板，使用真实数据调试界面
python3 main.py --gui-only

# 或添加执行权限后运行
chmod +x main.py
./main.py
```

## 使用说明

1. **启动应用** - 运行程序后，会在系统托盘显示图标
2. **查看统计** - 点击托盘图标打开详细面板
3. **右键菜单** - 右键点击托盘图标可查看快捷选项
4. **退出程序** - 右键菜单选择"退出程序"或使用 `Ctrl+C`

## 数据存储

统计数据存储在 `~/.config/keymouse-stats/stats.db` (SQLite数据库)

## 配置说明

编辑 `config.py` 文件可自定义以下配置：

- `RESET_TIME` - 每日重置时间 (默认 00:00)
- `HISTORY_DAYS` - 历史记录保留天数 (默认 7天)
- `TRAY_UPDATE_INTERVAL` - 托盘更新间隔 (秒)
- `MOUSE_MOVE_THRESHOLD` - 鼠标移动距离阈值 (像素)

## 系统要求

- Linux 操作系统
- Python 3.8+
- Qt5 运行时库
- X11 显示服务器 (支持系统托盘)

## 已知问题

- 仅支持X11会话，Wayland会话下系统托盘可能不工作
- 需要适当的系统权限来捕获输入事件

## 许可证

MIT License
