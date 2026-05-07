"""
定时任务调度器 - 每日自动重置
"""
import threading
import time
from datetime import datetime, timedelta
import config


class DailyResetScheduler:
    """每日重置调度器"""

    def __init__(self, tracker, on_reset_callback=None):
        self.tracker = tracker
        self.on_reset_callback = on_reset_callback
        self._stop_event = threading.Event()
        self._thread = None

    def _get_next_reset_time(self) -> datetime:
        """计算下一次重置时间"""
        now = datetime.now()
        reset_hour, reset_minute = map(int, config.RESET_TIME.split(':'))

        # 计算今天的重置时间
        reset_today = now.replace(hour=reset_hour, minute=reset_minute, second=0, microsecond=0)

        # 如果今天已经过了重置时间，则计算明天的
        if now >= reset_today:
            reset_today += timedelta(days=1)

        return reset_today

    def _run_scheduler(self):
        """运行调度器"""
        while not self._stop_event.is_set():
            next_reset = self._get_next_reset_time()
            wait_seconds = (next_reset - datetime.now()).total_seconds()

            if wait_seconds > 0:
                # 等待直到下一个重置时间
                self._stop_event.wait(timeout=wait_seconds)

            if not self._stop_event.is_set():
                # 执行重置
                self._do_reset()

    def _do_reset(self):
        """执行重置操作"""
        try:
            # 确保数据库有今日记录
            self.tracker.db.ensure_today_record()

            # 执行重置
            self.tracker.reset()

            # 回调通知
            if self.on_reset_callback:
                self.on_reset_callback()

        except Exception as e:
            print(f"重置失败: {e}")

    def start(self):
        """启动调度器"""
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()

    def stop(self):
        """停止调度器"""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
