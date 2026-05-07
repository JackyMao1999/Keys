#!/usr/bin/env python3
"""
KeyMouse Stats - Linux键盘鼠标统计应用
主入口文件 - 支持图形模式和命令行模式
"""
import sys
import os
import signal
import traceback
import argparse

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from database import Database
from stats_tracker import StatsTracker
from scheduler import DailyResetScheduler


class CLIStatsDisplay:
    """命令行统计显示"""

    def __init__(self, tracker):
        self.tracker = tracker
        self._running = True

    def _print_stats(self):
        """打印统计信息"""
        stats = self.tracker.get_formatted_stats()
        print("\n" + "=" * 40)
        print(f"📊 KeyMouse Stats - 今日统计")
        print("=" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("=" * 40)

    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print("\n\n收到退出信号，正在保存数据...")
        self._running = False
        self.tracker.stop()
        print("✓ 数据已保存")
        print("应用已安全退出")
        sys.exit(0)

    def run(self):
        """运行命令行模式"""
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        print(f"\n🚀 KeyMouse Stats 已启动 (命令行模式)")
        print("  - 程序在后台运行统计")
        print("  - 每5秒自动显示当前统计")
        print("  - 按 Ctrl+C 退出")
        print("  - 支持的统计:")
        print("    • 键盘敲击次数")
        print("    • 鼠标左键/右键点击")
        print("    • 鼠标移动距离")
        print("    • 滚动距离")
        print()

        # 启动追踪器
        self.tracker.start()
        print("✓ 统计追踪器已启动")
        print("\n" + "=" * 50)

        # 定期显示统计
        import time
        from datetime import datetime
        while self._running:
            try:
                # 打印当前时间戳
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 实时统计:")
                self._print_stats()
                print("=" * 50)
                time.sleep(5)  # 每5秒显示一次
            except KeyboardInterrupt:
                self._signal_handler(None, None)
                break


def check_display_available():
    """检查是否可用的图形界面"""
    display = os.environ.get('DISPLAY')
    wayland = os.environ.get('WAYLAND_DISPLAY')

    if display or wayland:
        # 检查Qt平台插件
        try:
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtCore import QCoreApplication
            app = QApplication([])
            app.quit()
            return True
        except Exception:
            pass

    return False


class Application:
    """应用主类"""

    def __init__(self, cli_mode=False):
        self.cli_mode = cli_mode

        # 初始化数据库
        self.db = Database(config.DB_PATH)

        # 初始化统计追踪器
        self.tracker = StatsTracker(self.db)

        # 初始化调度器
        self.scheduler = DailyResetScheduler(
            self.tracker,
            on_reset_callback=self._on_daily_reset
        )

        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print("\n收到退出信号，正在关闭...")
        self.shutdown()
        sys.exit(0)

    def _on_daily_reset(self):
        """每日重置回调"""
        from datetime import datetime
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 每日统计已重置")

    def startup(self):
        """启动应用"""
        print(f"正在启动 {config.APP_NAME}...")

        # 确保今日记录存在
        self.db.ensure_today_record()

        # 启动统计追踪器
        self.tracker.start()
        print("✓ 统计追踪器已启动")

        # 启动调度器
        self.scheduler.start()
        print("✓ 每日重置调度器已启动")

        print(f"✓ {config.APP_NAME} 已启动")

    def shutdown(self):
        """关闭应用"""
        print("\n正在关闭应用...")

        # 停止调度器
        self.scheduler.stop()

        # 停止追踪器
        self.tracker.stop()

        print("✓ 应用已安全退出")

    def run(self):
        """运行应用"""
        try:
            self.startup()

            if self.cli_mode or not check_display_available():
                # 命令行模式
                cli = CLIStatsDisplay(self.tracker)
                cli.run()
            else:
                # 图形界面模式
                from tray_app import TrayApp
                tray_app = TrayApp(self.tracker, self.db)
                tray_app.tray_icon.show()
                tray_app.app.exec_()

        except KeyboardInterrupt:
            self._signal_handler(None, None)
        except Exception as e:
            print(f"应用错误: {e}")
            traceback.print_exc()
            self.shutdown()
            sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='KeyMouse Stats - 键盘鼠标统计工具')
    parser.add_argument('--cli', action='store_true',
                        help='强制使用命令行模式（无GUI）')
    parser.add_argument('--gui', action='store_true',
                        help='强制使用GUI模式')
    args = parser.parse_args()

    cli_mode = args.cli
    if args.gui:
        cli_mode = False

    app = Application(cli_mode=cli_mode)
    app.run()


if __name__ == "__main__":
    main()
