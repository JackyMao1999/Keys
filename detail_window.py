"""
详细面板窗口 - 仪表盘布局 · 日期范围查询 · 键盘热力图
"""
from datetime import date, timedelta

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QSplitter, QGridLayout,
    QPushButton
)

import config
import settings
from keyboard_heatmap import KeyboardHeatmap
from settings_dialog import SettingsDialog


THEME_OPTIONS = {
    'light': '浅色',
    'dark': '深色',
    'blue': '蓝色',
    'green': '绿色',
    'mint': '薄荷',
    'aqua': '湖水',
    'lavender': '薰衣草',
    'peach': '蜜桃',
    'cream': '奶油',
}

THEMES = {
    'light': {'window': '#EEF2F7', 'panel': '#FFFFFF', 'panel_alt': '#F8FAFC', 'text': '#0F172A', 'muted': '#64748B', 'border': '#E2E8F0', 'button_border': '#CBD5E1', 'primary': '#3B82F6', 'primary_dark': '#2563EB', 'selected': '#EFF6FF', 'card_hover': '#F8FBFF'},
    'dark': {'window': '#0B1120', 'panel': '#111827', 'panel_alt': '#1E293B', 'text': '#F8FAFC', 'muted': '#94A3B8', 'border': '#334155', 'button_border': '#475569', 'primary': '#60A5FA', 'primary_dark': '#3B82F6', 'selected': '#1E3A8A', 'card_hover': '#172033'},
    'blue': {'window': '#EAF3FF', 'panel': '#FFFFFF', 'panel_alt': '#F0F7FF', 'text': '#0F2A43', 'muted': '#52708D', 'border': '#CFE4FF', 'button_border': '#A9CDF5', 'primary': '#1677FF', 'primary_dark': '#0958D9', 'selected': '#E6F4FF', 'card_hover': '#F5FAFF'},
    'green': {'window': '#ECFDF5', 'panel': '#FFFFFF', 'panel_alt': '#F0FDF4', 'text': '#052E16', 'muted': '#4B755D', 'border': '#BBF7D0', 'button_border': '#86EFAC', 'primary': '#16A34A', 'primary_dark': '#15803D', 'selected': '#DCFCE7', 'card_hover': '#F7FFF9'},
    'mint': {'window': '#EFFCF8', 'panel': '#FFFFFF', 'panel_alt': '#F2FBF7', 'text': '#123C35', 'muted': '#5B8178', 'border': '#C8F0E1', 'button_border': '#9EE6D0', 'primary': '#14B8A6', 'primary_dark': '#0F766E', 'selected': '#CCFBF1', 'card_hover': '#F8FFFC'},
    'aqua': {'window': '#ECFEFF', 'panel': '#FFFFFF', 'panel_alt': '#F0FDFF', 'text': '#123A47', 'muted': '#557887', 'border': '#BAE6FD', 'button_border': '#7DD3FC', 'primary': '#0891B2', 'primary_dark': '#0E7490', 'selected': '#CFFAFE', 'card_hover': '#F6FDFF'},
    'lavender': {'window': '#F7F3FF', 'panel': '#FFFFFF', 'panel_alt': '#FAF7FF', 'text': '#32204D', 'muted': '#74658F', 'border': '#E9D5FF', 'button_border': '#D8B4FE', 'primary': '#8B5CF6', 'primary_dark': '#7C3AED', 'selected': '#EDE9FE', 'card_hover': '#FCFAFF'},
    'peach': {'window': '#FFF7ED', 'panel': '#FFFFFF', 'panel_alt': '#FFF9F2', 'text': '#4A2A16', 'muted': '#8A6752', 'border': '#FED7AA', 'button_border': '#FDBA74', 'primary': '#F97316', 'primary_dark': '#EA580C', 'selected': '#FFEDD5', 'card_hover': '#FFFBF6'},
    'cream': {'window': '#FEFCE8', 'panel': '#FFFFFF', 'panel_alt': '#FFFDEA', 'text': '#3F3718', 'muted': '#7E7350', 'border': '#FDE68A', 'button_border': '#FACC15', 'primary': '#CA8A04', 'primary_dark': '#A16207', 'selected': '#FEF3C7', 'card_hover': '#FFFFF2'},
}


def build_stylesheet(theme_name: str) -> str:
    c = THEMES.get(theme_name, THEMES['light'])
    return f"""
QWidget {{ background-color: {c['window']}; font-family: "Segoe UI", "Noto Sans", "Ubuntu", sans-serif; color: {c['text']}; }}
QLabel {{ background: transparent; }}
QFrame#topBar, QFrame#leftPanel, QFrame#heatmapPanel {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 16px; }}
QFrame#statCard {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 14px; }}
QFrame#statCard:hover {{ border-color: {c['primary']}; background: {c['card_hover']}; }}
QPushButton {{ background: {c['panel']}; border: 1px solid {c['button_border']}; border-radius: 8px; padding: 6px 12px; color: {c['text']}; font-size: 12px; }}
QPushButton:hover {{ border-color: {c['primary']}; color: {c['primary']}; background: {c['panel_alt']}; }}
QPushButton:checked, QPushButton:pressed {{ background: {c['primary']}; border-color: {c['primary']}; color: white; }}
QDateEdit, QComboBox {{ background: {c['panel']}; border: 1px solid {c['button_border']}; border-radius: 10px; padding: 6px 30px 6px 10px; color: {c['text']}; font-size: 12px; min-height: 20px; }}
QDateEdit:hover, QComboBox:hover {{ border-color: {c['primary']}; background: {c['panel_alt']}; }}
QDateEdit:focus, QComboBox:focus {{ border: 1px solid {c['primary']}; }}
QComboBox::drop-down, QDateEdit::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 26px; border-left: 1px solid {c['border']}; border-top-right-radius: 9px; border-bottom-right-radius: 9px; background: {c['panel_alt']}; }}
QComboBox::down-arrow, QDateEdit::down-arrow {{ width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid {c['muted']}; margin-right: 8px; }}
QComboBox QAbstractItemView {{ background: {c['panel']}; color: {c['text']}; border: 1px solid {c['border']}; border-radius: 10px; padding: 6px; outline: none; selection-background-color: {c['selected']}; }}
QComboBox QAbstractItemView::item {{ min-height: 26px; padding: 6px 10px; border-radius: 6px; }}
QComboBox QAbstractItemView::item:hover {{ background: {c['panel_alt']}; color: {c['primary']}; }}
QComboBox QAbstractItemView::item:selected {{ background: {c['selected']}; color: {c['primary']}; }}
QCalendarWidget QWidget {{ alternate-background-color: {c['panel_alt']}; }}
QCalendarWidget QToolButton {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 8px; color: {c['text']}; margin: 2px; padding: 5px 8px; }}
QCalendarWidget QToolButton:hover {{ background: {c['panel_alt']}; color: {c['primary']}; border-color: {c['primary']}; }}
QCalendarWidget QMenu {{ background: {c['panel']}; color: {c['text']}; border: 1px solid {c['border']}; border-radius: 8px; }}
QCalendarWidget QSpinBox {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 8px; padding: 4px 8px; color: {c['text']}; }}
QCalendarWidget QAbstractItemView {{ background: {c['panel']}; color: {c['text']}; border: none; selection-background-color: {c['primary']}; selection-color: white; outline: none; }}
QCalendarWidget QAbstractItemView:enabled {{ alternate-background-color: {c['panel_alt']}; }}
QTableWidget {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 12px; gridline-color: {c['border']}; font-size: 12px; selection-background-color: {c['selected']}; }}
QTableWidget::item {{ padding: 5px 8px; }}
QTableWidget::item:selected {{ background: {c['selected']}; color: {c['text']}; }}
QHeaderView::section {{ background: {c['panel_alt']}; border: none; border-bottom: 1px solid {c['border']}; padding: 7px 8px; font-weight: 700; color: {c['muted']}; }}
QScrollBar:vertical {{ background: transparent; width: 8px; margin: 4px 2px 4px 2px; }}
QScrollBar::handle:vertical {{ background: {c['button_border']}; border-radius: 4px; min-height: 28px; }}
QScrollBar::handle:vertical:hover {{ background: {c['primary']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; background: transparent; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
QScrollBar:horizontal {{ background: transparent; height: 8px; margin: 2px 4px 2px 4px; }}
QScrollBar::handle:horizontal {{ background: {c['button_border']}; border-radius: 4px; min-width: 28px; }}
QScrollBar::handle:horizontal:hover {{ background: {c['primary']}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; background: transparent; }}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: transparent; }}
QSplitter::handle {{ background: transparent; }}
"""


class StatCard(QFrame):
    """统计卡片。"""

    def __init__(self, label: str, value: str, accent: str = '#3B82F6'):
        super().__init__()
        self.setObjectName('statCard')
        self.setMinimumSize(142, 84)
        self.accent = accent

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        self.label = QLabel(label)
        self.label.setStyleSheet('background: transparent; color: #64748B; font-size: 12px; font-weight: 600;')

        self.value = QLabel(value)
        self.value.setStyleSheet(f'background: transparent; color: {self.accent}; font-size: 21px; font-weight: 800;')

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.value)

    def set_value(self, text: str):
        self.value.setText(text)

    def set_theme(self, theme: dict):
        self.label.setStyleSheet(f"background: transparent; color: {theme['muted']}; font-size: 12px; font-weight: 600;")
        self.value.setStyleSheet(f"background: transparent; color: {self.accent}; font-size: 21px; font-weight: 800;")


class DetailWindow(QWidget):
    """详细统计面板。"""

    def __init__(self, tracker, db, parent=None):
        super().__init__(parent)
        self.tracker = tracker
        self.db = db
        self.current_start = date.today()
        self.current_end = date.today()
        self.current_theme = settings.get_theme()
        if self.current_theme not in THEMES:
            self.current_theme = 'light'

        self.setWindowTitle(config.APP_NAME)
        self.setFixedSize(1200, 720)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

        self._init_ui()
        self._apply_theme(save=False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_display)
        self.timer.start(1000)

        self._refresh_current_range(force=True)

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(12)

        root.addWidget(self._create_top_bar())

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(10)
        splitter.addWidget(self._create_left_panel())
        splitter.addWidget(self._create_heatmap_panel())
        splitter.setSizes([360, 760])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter, 1)

    def _create_top_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName('topBar')
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        self.main_title = QLabel('KeyMouse Stats')
        self.range_title = QLabel('今日统计')
        title_box.addWidget(self.main_title)
        title_box.addWidget(self.range_title)
        layout.addLayout(title_box)
        layout.addStretch()

        for text, handler in [
            ('今天', self._select_today),
            ('昨天', self._select_yesterday),
            ('最近7天', self._select_recent_7_days),
            ('本月', self._select_this_month),
            ('今年', self._select_this_year),
            ('所有', self._select_all),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            layout.addWidget(btn)

        settings_btn = QPushButton('设置')
        settings_btn.clicked.connect(self._show_settings)
        layout.addWidget(settings_btn)
        return bar

    def _create_left_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName('leftPanel')
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.overview_title = QLabel('统计总览')
        layout.addWidget(self.overview_title)

        grid = QGridLayout()
        grid.setSpacing(10)
        self.cards = {}
        cards = [
            ('keyboard', '键盘敲击', '0 次', '#2563EB'),
            ('left_click', '鼠标左键', '0 次', '#059669'),
            ('right_click', '鼠标右键', '0 次', '#7C3AED'),
            ('move', '鼠标移动', '0 cm', '#EA580C'),
            ('scroll', '滚动距离', '0', '#0F766E'),
            ('total_clicks', '鼠标点击', '0 次', '#DC2626'),
        ]
        for i, (key, label, value, accent) in enumerate(cards):
            card = StatCard(label, value, accent)
            self.cards[key] = card
            grid.addWidget(card, i // 2, i % 2)
        layout.addLayout(grid)

        self.table_title = QLabel('每日明细')
        layout.addWidget(self.table_title)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(['日期', '键盘', '左键', '右键', '移动', '滚动'])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.history_table, 1)
        return panel

    def _create_heatmap_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName('heatmapPanel')
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.heatmap = KeyboardHeatmap()
        layout.addWidget(self.heatmap)
        return panel

    def _apply_theme(self, save: bool = True):
        theme = THEMES.get(self.current_theme, THEMES['light'])
        self.setStyleSheet(build_stylesheet(self.current_theme))
        if save:
            settings.set_theme(self.current_theme)

        if hasattr(self, 'main_title'):
            self.main_title.setStyleSheet(
                f"background: transparent; font-size: 22px; font-weight: 900; color: {theme['text']};"
            )
            self.range_title.setStyleSheet(
                f"background: transparent; color: {theme['muted']}; font-size: 12px;"
            )
            self.overview_title.setStyleSheet(
                f"background: transparent; color: {theme['text']}; font-size: 15px; font-weight: 800;"
            )
            self.table_title.setStyleSheet(
                f"background: transparent; color: {theme['text']}; font-size: 15px; font-weight: 800;"
            )
            for card in self.cards.values():
                card.set_theme(theme)
            if hasattr(self.heatmap, 'set_theme'):
                self.heatmap.set_theme(self.current_theme)

    def _show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            self.current_theme = settings.get_theme()
            if self.current_theme not in THEMES:
                self.current_theme = 'light'
            self._apply_theme(save=False)
            self.tracker.configure_notifications(
                settings.get_notifications_enabled(),
                settings.get_notification_threshold()
            )

    def _select_today(self):
        today = date.today()
        self._set_range(today, today)

    def _select_yesterday(self):
        yesterday = date.today() - timedelta(days=1)
        self._set_range(yesterday, yesterday)

    def _select_recent_7_days(self):
        today = date.today()
        self._set_range(today - timedelta(days=6), today)

    def _select_this_month(self):
        today = date.today()
        self._set_range(today.replace(day=1), today)

    def _select_this_year(self):
        today = date.today()
        self._set_range(today.replace(month=1, day=1), today)

    def _select_all(self):
        today = date.today()
        bounds = self.db.get_date_bounds()
        start_text = bounds.get('start_date')
        try:
            start = date.fromisoformat(start_text) if start_text else today
        except ValueError:
            start = today
        self._set_range(start, today)

    def _set_range(self, start: date, end: date):
        self.current_start = start
        self.current_end = end
        self._refresh_current_range(force=True)

    def _update_display(self):
        if self.current_end >= date.today():
            self._refresh_current_range(force=False)

    def _refresh_current_range(self, force=False):
        stats, key_stats, daily_rows = self._query_current_range()
        label = self._range_label(self.current_start, self.current_end)
        self.range_title.setText(label)
        self._update_cards(stats)
        self._update_history_table(daily_rows)
        self.heatmap.set_context(label, stats.get('key_presses', 0))
        self.heatmap.set_key_stats(key_stats)

    def _query_current_range(self):
        today = date.today()
        start_s = self.current_start.isoformat()
        end_s = self.current_end.isoformat()

        if self.current_end < today:
            stats = self.db.get_stats_by_date_range(start_s, end_s)
            key_stats = self.db.get_key_stats_by_date_range(start_s, end_s)
            daily = self.db.get_daily_stats_by_date_range(start_s, end_s)
            return stats, key_stats, daily

        if self.current_start > today:
            return self._empty_stats(), {}, []

        tracker_stats = self.tracker.get_stats()
        today_row = self._today_row_from_tracker(tracker_stats)

        if self.current_start == today:
            return tracker_stats, tracker_stats.get('key_detail', {}), [today_row]

        historical_end = today - timedelta(days=1)
        stats = self.db.get_stats_by_date_range(start_s, historical_end.isoformat())
        key_stats = self.db.get_key_stats_by_date_range(start_s, historical_end.isoformat())
        daily = self.db.get_daily_stats_by_date_range(start_s, historical_end.isoformat())

        self._merge_stats(stats, tracker_stats)
        self._merge_key_stats(key_stats, tracker_stats.get('key_detail', {}))
        return stats, key_stats, [today_row] + daily

    def _empty_stats(self):
        return {
            'key_presses': 0,
            'mouse_left_clicks': 0,
            'mouse_right_clicks': 0,
            'mouse_move_distance': 0.0,
            'scroll_distance': 0,
            'total_clicks': 0,
        }

    def _merge_stats(self, base: dict, extra: dict):
        for key in ['key_presses', 'mouse_left_clicks', 'mouse_right_clicks', 'mouse_move_distance', 'scroll_distance']:
            base[key] = base.get(key, 0) + extra.get(key, 0)
        base['total_clicks'] = base.get('mouse_left_clicks', 0) + base.get('mouse_right_clicks', 0)

    def _merge_key_stats(self, base: dict, extra: dict):
        for key, value in extra.items():
            base[key] = base.get(key, 0) + value

    def _today_row_from_tracker(self, stats: dict) -> dict:
        return {
            'date': date.today().isoformat(),
            'key_presses': stats.get('key_presses', 0),
            'mouse_left_clicks': stats.get('mouse_left_clicks', 0),
            'mouse_right_clicks': stats.get('mouse_right_clicks', 0),
            'mouse_move_distance': stats.get('mouse_move_distance', 0.0),
            'scroll_distance': stats.get('scroll_distance', 0),
        }

    def _update_cards(self, stats: dict):
        self.cards['keyboard'].set_value(f"{int(stats.get('key_presses', 0)):,} 次")
        self.cards['left_click'].set_value(f"{int(stats.get('mouse_left_clicks', 0)):,} 次")
        self.cards['right_click'].set_value(f"{int(stats.get('mouse_right_clicks', 0)):,} 次")
        self.cards['move'].set_value(self._format_distance(stats.get('mouse_move_distance', 0.0)))
        self.cards['scroll'].set_value(f"{int(stats.get('scroll_distance', 0)):,}")
        self.cards['total_clicks'].set_value(f"{int(stats.get('total_clicks', 0)):,} 次")

    def _update_history_table(self, rows: list):
        self.history_table.setRowCount(len(rows))
        for i, record in enumerate(rows):
            self.history_table.setItem(i, 0, QTableWidgetItem(record.get('date', '')))
            self.history_table.setItem(i, 1, QTableWidgetItem(f"{int(record.get('key_presses', 0)):,}"))
            self.history_table.setItem(i, 2, QTableWidgetItem(f"{int(record.get('mouse_left_clicks', 0)):,}"))
            self.history_table.setItem(i, 3, QTableWidgetItem(f"{int(record.get('mouse_right_clicks', 0)):,}"))
            self.history_table.setItem(i, 4, QTableWidgetItem(self._format_distance(record.get('mouse_move_distance', 0.0))))
            self.history_table.setItem(i, 5, QTableWidgetItem(f"{int(record.get('scroll_distance', 0)):,}"))

    def _range_label(self, start: date, end: date) -> str:
        today = date.today()
        if start == end == today:
            return '今日统计'
        if start == end:
            return f'{start.isoformat()} 统计'
        return f'{start.isoformat()} 至 {end.isoformat()} 统计'

    def _format_distance(self, pixels: float) -> str:
        cm = pixels * 2.54 / 96
        if cm >= 100:
            return f'{cm / 100:.1f} m'
        if cm >= 1:
            return f'{cm:.1f} cm'
        return f'{cm * 10:.1f} mm'

    def closeEvent(self, event):
        event.ignore()
        self.hide()
