---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100f6269bb78d70fc8682250abda7fc039f2dc1580071c33b9949599992eaacf77a0221008c4fc971aa8cb44ff769438e453659d269f290e93d20815ddb04e5a5b20f6ed8
    ReservedCode2: 3045022017f9f81f09d1be9ea830d4233bd1762de666a6d51510e99d0b0ebac9336135ad022100b6c35c8ef7f272bed81e891c7a9cd2902056593906477752849f52fa78a795f2
---

# KeyMouse Stats - Linux键盘鼠标统计应用

## 1. 项目概述

- **项目名称**: KeyMouse Stats
- **项目类型**: Linux桌面后台应用 (系统托盘)
- **核心功能**: 实时统计键盘按键、鼠标点击、鼠标移动距离、页面滚动距离，显示在系统托盘菜单栏
- **目标用户**: 需要了解自己电脑使用习惯的用户

## 2. 技术栈

- **编程语言**: Python 3.8+
- **GUI框架**: PyQt5 (系统托盘 + 详细面板)
- **事件捕获**: pynput (键盘、鼠标事件监听)
- **数据存储**: SQLite (轻量、跨平台、持久化)
- **定时任务**: schedule (每日自动重置)

## 3. 功能列表

### 3.1 核心统计功能
| 功能 | 描述 | 实现方式 |
|------|------|----------|
| 键盘敲击统计 | 实时统计每日键盘按键总次数 | pynput.keyboard.Listener |
| 鼠标点击统计 | 分别统计左键/右键点击次数 | pynput.mouse.Listener |
| 鼠标移动距离 | 追踪鼠标移动的总像素距离 | 记录连续位置点计算欧几里得距离 |
| 滚动距离统计 | 记录滚轮滚动的累计单位数 | pynput.mouse.Listener on_scroll |

### 3.2 UI显示功能
| 功能 | 描述 |
|------|------|
| 菜单栏显示 | 系统托盘图标旁显示今日总按键数 |
| 托盘菜单 | 右键菜单：显示各统计数据入口 |
| 详细面板 | 独立窗口显示完整统计信息 |

### 3.3 数据管理
| 功能 | 描述 |
|------|------|
| 每日自动重置 | 每天午夜0点自动重置当日统计数据 |
| 数据持久化 | 使用SQLite存储，程序重启后数据不丢失 |
| 历史记录 | 保留每日统计数据用于历史查询 |

## 4. UI/UX设计

### 4.1 布局结构
- **系统托盘**: 主入口，显示总按键数
- **右键菜单**: 快速访问选项
- **详情窗口**: 独立窗口显示完整统计

### 4.2 视觉风格
- **主题**: 系统原生GTK主题
- **托盘图标**: 自定义统计图标 (显示数字徽章)
- **窗口**: 标准Qt窗口，简洁现代

### 4.3 窗口设计
```
┌─────────────────────────────────────┐
│  📊 KeyMouse Stats 今日统计          │
├─────────────────────────────────────┤
│  键盘敲击      │  12,345 次          │
│  鼠标左键      │  5,678 次           │
│  鼠标右键      │  1,234 次           │
│  鼠标移动      │  45.2 万像素        │
│  滚动距离      │  3,456 单位         │
├─────────────────────────────────────┤
│  📅 历史记录 (最近7天)               │
│  2024-01-15: 按键 12000, 点击 5000  │
│  2024-01-14: 按键 11000, 点击 4800  │
├─────────────────────────────────────┤
│  [退出程序]                          │
└─────────────────────────────────────┘
```

## 5. 数据模型

### 5.1 数据库表结构
```sql
CREATE TABLE daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE NOT NULL,
    key_presses INTEGER DEFAULT 0,
    mouse_left_clicks INTEGER DEFAULT 0,
    mouse_right_clicks INTEGER DEFAULT 0,
    mouse_move_distance REAL DEFAULT 0.0,
    scroll_distance INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 6. 模块架构

```
keymouse-stats/
├── main.py              # 主入口
├── config.py            # 配置常量
├── database.py          # SQLite数据库操作
├── stats_tracker.py     # 统计追踪器(核心逻辑)
├── tray_app.py          # 系统托盘应用
├── detail_window.py     # 详细面板窗口
├── scheduler.py         # 定时任务(每日重置)
├── requirements.txt     # 依赖列表
├── SPEC.md              # 本文档
└── README.md            # 使用说明
```

## 7. 验收标准

- [x] 程序可以在Linux系统托盘运行
- [x] 可以正确捕获并统计键盘按键
- [x] 可以正确区分并统计鼠标左右键点击
- [x] 可以计算鼠标移动距离(像素)
- [x] 可以统计滚轮滚动距离
- [x] 托盘图标显示今日总按键数
- [x] 点击托盘图标打开详情窗口
- [x] 午夜自动重置统计数据
- [x] 关闭程序后重新打开数据不丢失
- [x] 显示最近7天历史记录
