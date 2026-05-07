"""
系统托盘应用 - 简洁UI设计
"""
import os
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor, QFont
from datetime import date
import config
from detail_window import DetailWindow


class TrayApp:
    """系统托盘应用管理"""

    def __init__(self, tracker, db):
        self.tracker = tracker
        self.db = db
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # 设置应用信息
        self.app.setApplicationName(config.APP_NAME)
        self.app.setApplicationVersion(config.APP_VERSION)

        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self._create_icon("0"))
        self.tray_icon.setToolTip(f"{config.APP_NAME}\n今日统计就绪")

        # 创建右键菜单
        self._create_menu()

        # 创建详情窗口
        self.detail_window = DetailWindow(tracker, db)

        # 托盘点击事件
        self.tray_icon.activated.connect(self._on_tray_activated)

        # 定时更新托盘提示
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_tray_icon)
        self.update_timer.start(config.TRAY_UPDATE_INTERVAL * 1000)

    def _create_icon(self, text: str) -> QIcon:
        """创建简洁托盘图标"""
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制圆形背景 (简洁蓝色)
        painter.setBrush(QColor(70, 130, 180))  # SteelBlue
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, size - 4, size - 4)

        # 绘制简洁键盘轮廓
        painter.setBrush(QColor(255, 255, 255, 220))
        # 键盘主体 - 使用普通矩形
        painter.drawRect(14, 18, 36, 22)

        # 绘制键位
        painter.setBrush(QColor(180, 180, 200))
        for row in range(3):
            for col in range(5):
                painter.drawRect(16 + col * 7, 20 + row * 6, 5, 4)

        # 如果文本不为0，显示数字徽章
        if text != "0" and text:
            # 红色徽章背景
            painter.setBrush(QColor(220, 53, 69))  # 红色
            painter.drawEllipse(size - 24, 0, 24, 24)

            # 绘制数字
            font = QFont()
            font.setPointSize(9)
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(size - 24, 0, 24, 24, Qt.AlignCenter, text[-3:] if len(text) > 3 else text)

        painter.end()
        return QIcon(pixmap)

    def _create_menu(self):
        """创建简洁右键菜单"""
        menu = QMenu()

        # 标题
        title_action = QAction(f"{config.APP_NAME} v{config.APP_VERSION}", menu)
        title_action.setEnabled(False)
        menu.addAction(title_action)
        menu.addSeparator()

        # 今日统计
        stats_action = QAction(f"键盘敲击: 0", menu)
        stats_action.setEnabled(False)
        menu.addAction(stats_action)
        self.menu_stat_labels = {
            'keyboard': stats_action,
            'left_click': QAction(f"鼠标左键: 0", menu),
            'right_click': QAction(f"鼠标右键: 0", menu),
            'move': QAction(f"鼠标移动: 0", menu),
            'scroll': QAction(f"滚动距离: 0", menu),
        }
        for action in [self.menu_stat_labels['left_click'], self.menu_stat_labels['right_click'],
                       self.menu_stat_labels['move'], self.menu_stat_labels['scroll']]:
            action.setEnabled(False)
            menu.addAction(action)

        menu.addSeparator()

        # 查看详情
        detail_action = QAction("查看详情面板", menu)
        detail_action.triggered.connect(self._show_detail)
        menu.addAction(detail_action)
        menu.addSeparator()

        # 退出
        quit_action = QAction("退出程序", menu)
        quit_action.triggered.connect(self._quit_app)
        menu.addAction(quit_action)

        self.tray_icon.setContextMenu(menu)

    def _update_tray_icon(self):
        """更新托盘图标和菜单"""
        stats = self.tracker.get_stats()
        total = stats['key_presses']

        # 更新图标
        self.tray_icon.setIcon(self._create_icon(str(total)))

        # 更新工具提示
        self.tray_icon.setToolTip(
            f"{config.APP_NAME}\n"
            f"日期: {date.today().isoformat()}\n"
            f"键盘: {total:,} 次"
        )

        # 更新菜单统计
        if hasattr(self, 'menu_stat_labels'):
            self.menu_stat_labels['keyboard'].setText(f"键盘敲击: {stats['key_presses']:,}")
            self.menu_stat_labels['left_click'].setText(f"鼠标左键: {stats['mouse_left_clicks']:,}")
            self.menu_stat_labels['right_click'].setText(f"鼠标右键: {stats['mouse_right_clicks']:,}")
            self.menu_stat_labels['move'].setText(f"鼠标移动: {self._format_distance(stats['mouse_move_distance'])}")
            self.menu_stat_labels['scroll'].setText(f"滚动距离: {stats['scroll_distance']:,}")

    def _format_distance(self, pixels: float) -> str:
        """格式化距离 - 转换为厘米"""
        cm = pixels * 2.54 / 96
        if cm >= 100:
            return f"{cm / 100:.1f} m"
        elif cm >= 1:
            return f"{cm:.1f} cm"
        else:
            return f"{cm * 10:.1f} mm"

    def _on_tray_activated(self, reason):
        """托盘图标点击事件"""
        if reason == QSystemTrayIcon.Trigger:  # 左键单击
            self._show_detail()
        elif reason == QSystemTrayIcon.Context:  # 右键
            pass  # 会自动显示菜单

    def _show_detail(self):
        """显示详情窗口"""
        self.detail_window.show()
        self.detail_window.raise_()
        self.detail_window.activateWindow()

    def _show_about(self):
        """显示关于对话框"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(
            self.detail_window,
            f"关于 {config.APP_NAME}",
            f"<h3>{config.APP_NAME}</h3>"
            f"<p>版本: {config.APP_VERSION}</p>"
            f"<p>一款简洁的键盘鼠标使用统计工具。</p>"
            f"<p>帮助您了解每日的电脑使用习惯。</p>"
            f"<p style='color:gray;'>© 2024</p>"
        )

    def _quit_app(self):
        """退出应用"""
        self.tracker.stop()
        self.app.quit()

    def run(self):
        """运行应用"""
        self.tray_icon.show()
        self.app.exec_()
