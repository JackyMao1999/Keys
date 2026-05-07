"""
统计追踪器 - 核心事件捕获逻辑
"""
import math
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
from typing import Optional
import config


class StatsTracker:
    """键盘鼠标统计追踪器"""

    # 每 N 次按键批量写入逐键数据
    KEY_DETAIL_FLUSH_INTERVAL = 60
    # 每 N 次按键批量更新总按键数
    TOTAL_KEY_FLUSH_INTERVAL = 10

    def __init__(self, db, on_update_callback=None):
        self.db = db
        self.on_update_callback = on_update_callback

        # 状态追踪
        self._key_presses = 0
        self._mouse_left_clicks = 0
        self._mouse_right_clicks = 0
        self._mouse_move_distance = 0.0
        self._scroll_distance = 0

        # 逐键追踪: {key_name: count}
        self._key_detail = {}          # 今日完整累计 (不清空)
        self._key_detail_pending = {}  # 待写入DB的增量
        self._key_detail_since_flush = 0

        # 鼠标位置追踪
        self._last_mouse_x = None
        self._last_mouse_y = None

        # Listeners
        self._keyboard_listener = None
        self._mouse_listener = None

        # 加载今日数据
        self._load_today_data()

    def _load_today_data(self):
        """从数据库加载今日数据"""
        stats = self.db.get_today_stats()
        self._key_presses = stats.get('key_presses', 0)
        self._mouse_left_clicks = stats.get('mouse_left_clicks', 0)
        self._mouse_right_clicks = stats.get('mouse_right_clicks', 0)
        self._mouse_move_distance = stats.get('mouse_move_distance', 0.0)
        self._scroll_distance = stats.get('scroll_distance', 0)

        # 加载逐键数据
        self._key_detail = self.db.get_today_key_stats()

    def _notify_update(self):
        """通知数据更新"""
        if self.on_update_callback:
            self.on_update_callback(self.get_stats())

    def _normalize_key_name(self, key) -> str:
        """将 pynput key 对象归一化为字符串标识符"""
        try:
            if hasattr(key, 'char') and key.char:
                return key.char.lower()
            elif hasattr(key, 'name') and key.name:
                return key.name.lower()
        except Exception:
            pass
        return str(key).lower()

    def _on_key_press(self, key):
        """键盘按键回调"""
        if isinstance(key, (Key, KeyCode)):
            self._key_presses += 1

            # 逐键统计
            key_name = self._normalize_key_name(key)
            if key_name:
                self._key_detail[key_name] = self._key_detail.get(key_name, 0) + 1
                self._key_detail_pending[key_name] = self._key_detail_pending.get(key_name, 0) + 1
                self._key_detail_since_flush += 1
                if self._key_detail_since_flush >= self.KEY_DETAIL_FLUSH_INTERVAL:
                    self._flush_key_detail()

            # 批量更新数据库 (每10次更新一次，减少IO)
            if self._key_presses % self.TOTAL_KEY_FLUSH_INTERVAL == 0:
                self.db.update_stats(key_presses=self.TOTAL_KEY_FLUSH_INTERVAL)
            self._notify_update()

    def _on_key_release(self, key):
        """键盘释放回调"""
        pass

    def _on_mouse_click(self, x, y, button, pressed):
        """鼠标点击回调"""
        if pressed:
            if button == mouse.Button.left:
                self._mouse_left_clicks += 1
                self.db.update_stats(mouse_left_clicks=1)
            elif button == mouse.Button.right:
                self._mouse_right_clicks += 1
                self.db.update_stats(mouse_right_clicks=1)
            self._notify_update()

    def _on_mouse_move(self, x, y):
        """鼠标移动回调"""
        if self._last_mouse_x is not None and self._last_mouse_y is not None:
            # 计算欧几里得距离
            dx = x - self._last_mouse_x
            dy = y - self._last_mouse_y
            distance = math.sqrt(dx * dx + dy * dy)

            # 只有超过阈值才计入
            if distance >= config.MOUSE_MOVE_THRESHOLD:
                self._mouse_move_distance += distance
                # 批量更新 (每100像素更新一次)
                if int(self._mouse_move_distance) % 100 == 0:
                    self.db.update_stats(mouse_move_distance=100)
                self._notify_update()

        self._last_mouse_x = x
        self._last_mouse_y = y

    def _on_mouse_scroll(self, x, y, dx, dy):
        """鼠标滚轮回调"""
        # dy表示垂直滚动量
        self._scroll_distance += abs(int(dy))
        # 批量更新 (每5个单位更新一次)
        if self._scroll_distance % 5 == 0:
            self.db.update_stats(scroll_distance=5)
        self._notify_update()

    def start(self):
        """启动追踪器"""
        # 创建键盘监听器
        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self._keyboard_listener.start()

        # 创建鼠标监听器
        self._mouse_listener = mouse.Listener(
            on_click=self._on_mouse_click,
            on_move=self._on_mouse_move,
            on_scroll=self._on_mouse_scroll
        )
        self._mouse_listener.start()

    def stop(self):
        """停止追踪器"""
        # 保存剩余数据
        self._save_remaining_stats()

        if self._keyboard_listener:
            self._keyboard_listener.stop()
            self._keyboard_listener = None

        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None

    def _flush_key_detail(self):
        """将增量逐键数据写入数据库"""
        if self._key_detail_pending:
            self.db.flush_key_stats(self._key_detail_pending)
            self._key_detail_pending.clear()
        self._key_detail_since_flush = 0

    def _save_remaining_stats(self):
        """保存剩余未批量更新的统计数据"""
        # 先刷新逐键增量数据
        self._flush_key_detail()

        # 计算剩余需要保存的总量
        key_mod = self._key_presses % self.TOTAL_KEY_FLUSH_INTERVAL
        if key_mod > 0:
            self.db.update_stats(key_presses=key_mod)

        dist_mod = int(self._mouse_move_distance) % 100
        if dist_mod >= config.MOUSE_MOVE_THRESHOLD:
            self.db.update_stats(mouse_move_distance=dist_mod)

        scroll_mod = self._scroll_distance % 5
        if scroll_mod > 0:
            self.db.update_stats(scroll_distance=scroll_mod)

    def reset(self):
        """重置统计数据"""
        self._key_presses = 0
        self._mouse_left_clicks = 0
        self._mouse_right_clicks = 0
        self._mouse_move_distance = 0.0
        self._scroll_distance = 0
        self._key_detail.clear()
        self._key_detail_pending.clear()
        self._key_detail_since_flush = 0
        self._last_mouse_x = None
        self._last_mouse_y = None
        self.db.reset_today_stats()
        self.db.reset_today_key_stats()
        self._notify_update()

    def get_stats(self) -> dict:
        """获取当前统计数据"""
        return {
            'key_presses': self._key_presses,
            'mouse_left_clicks': self._mouse_left_clicks,
            'mouse_right_clicks': self._mouse_right_clicks,
            'mouse_move_distance': self._mouse_move_distance,
            'scroll_distance': self._scroll_distance,
            'total_clicks': self._mouse_left_clicks + self._mouse_right_clicks,
            'key_detail': dict(self._key_detail)
        }

    def get_formatted_stats(self) -> dict:
        """获取格式化后的统计数据"""
        stats = self.get_stats()
        return {
            '键盘敲击': f"{stats['key_presses']:,} 次",
            '鼠标左键': f"{stats['mouse_left_clicks']:,} 次",
            '鼠标右键': f"{stats['mouse_right_clicks']:,} 次",
            '鼠标移动': self._format_distance(stats['mouse_move_distance']),
            '滚动距离': f"{stats['scroll_distance']:,} 单位"
        }

    def _format_distance(self, pixels: float) -> str:
        """格式化距离显示 - 将像素转换为厘米"""
        # 屏幕通常约96 DPI: 96像素 = 1英寸 = 2.54厘米
        cm = pixels * 2.54 / 96
        if cm >= 100:
            return f"{cm / 100:.1f} m"
        elif cm >= 1:
            return f"{cm:.1f} cm"
        else:
            return f"{cm * 10:.1f} mm"
