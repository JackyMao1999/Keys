"""
配置文件 - KeyMouse Stats
"""
import os

# 应用配置
APP_NAME = "KeyMouse Stats"
APP_VERSION = "1.0.0"

# 数据库配置
DB_PATH = os.path.expanduser("~/.config/keymouse-stats/stats.db")

# 统计重置时间 (小时:分钟)
RESET_TIME = "00:00"

# 历史记录保留天数
HISTORY_DAYS = 7

# 托盘图标更新间隔 (秒)
TRAY_UPDATE_INTERVAL = 1

# 鼠标移动距离采样阈值 (像素)
# 只有移动超过这个距离才计入，防止微小抖动
MOUSE_MOVE_THRESHOLD = 2

# 日志配置
LOG_PATH = os.path.expanduser("~/.config/keymouse-stats/app.log")
LOG_LEVEL = "INFO"
