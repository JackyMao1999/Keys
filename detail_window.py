"""
详细面板窗口 - 仪表盘布局 · 日期范围查询 · 键盘热力图
"""
from datetime import date, timedelta

from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QSplitter, QGridLayout,
    QPushButton, QDateEdit
)

import config
from keyboard_heatmap import KeyboardHeatmap


STYLESHEET = """
QWidget {
    background-color: #EEF2F7;
    font-family: "Segoe UI", "Noto Sans", "Ubuntu", sans-serif;
    color: #0F172A;
}

QLabel {
    background: transparent;
}

QFrame#topBar, QFrame#leftPanel, QFrame#heatmapPanel {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
}

QFrame#statCard {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
}
QFrame#statCard:hover {
    border-color: #93C5FD;
    background: #F8FBFF;
}

QPushButton {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 6px 12px;
    color: #334155;
    font-size: 12px;
}
QPushButton:hover {
    border-color: #3B82F6;
    color: #2563EB;
    background: #F8FAFC;
}
QPushButton:checked, QPushButton:pressed {
    background: #3B82F6;
    border-color: #3B82F6;
    color: white;
}

QDateEdit {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 5px 9px;
    color: #1E293B;
    font-size: 12px;
}
QDateEdit:hover {
    border-color: #3B82F6;
}

QTableWidget {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    gridline-color: #F1F5F9;
    font-size: 12px;
    selection-background-color: #EFF6FF;
}
QTableWidget::item {
    padding: 5px 8px;
}
QTableWidget::item:selected {
    background: #EFF6FF;
    color: #0F172A;
}
QHeaderView::section {
    background: #F8FAFC;
    border: none;
    border-bottom: 1px solid #E2E8F0;
    padding: 7px 8px;
    font-weight: 700;
    color: #64748B;
}

QSplitter::handle {
    background: transparent;
}
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


class DetailWindow(QWidget):
    """详细统计面板。"""

    def __init__(self, tracker, db, parent=None):
        super().__init__(parent)
        self.tracker = tracker
        self.db = db
        self.current_start = date.today()
        self.current_end = date.today()

        self.setWindowTitle(config.APP_NAME)
        self.setMinimumSize(1120, 640)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(STYLESHEET)

        self._init_ui()

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
        title = QLabel('KeyMouse Stats')
        title.setStyleSheet('background: transparent; font-size: 22px; font-weight: 900; color: #0F172A;')
        self.range_title = QLabel('今日统计')
        self.range_title.setStyleSheet('background: transparent; color: #64748B; font-size: 12px;')
        title_box.addWidget(title)
        title_box.addWidget(self.range_title)
        layout.addLayout(title_box)
        layout.addStretch()

        for text, handler in [
            ('今天', self._select_today),
            ('昨天', self._select_yesterday),
            ('最近7天', self._select_recent_7_days),
            ('本月', self._select_this_month),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            layout.addWidget(btn)

        self.start_edit = QDateEdit()
        self.end_edit = QDateEdit()
        for edit in (self.start_edit, self.end_edit):
            edit.setCalendarPopup(True)
            edit.setDisplayFormat('yyyy-MM-dd')
            edit.setDate(QDate.currentDate())

        layout.addWidget(QLabel('从'))
        layout.addWidget(self.start_edit)
        layout.addWidget(QLabel('到'))
        layout.addWidget(self.end_edit)

        query_btn = QPushButton('查询')
        query_btn.clicked.connect(self._select_custom_range)
        layout.addWidget(query_btn)
        return bar

    def _create_left_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName('leftPanel')
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        section = QLabel('统计总览')
        section.setStyleSheet('background: transparent; color: #334155; font-size: 15px; font-weight: 800;')
        layout.addWidget(section)

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

        table_title = QLabel('每日明细')
        table_title.setStyleSheet('background: transparent; color: #334155; font-size: 15px; font-weight: 800;')
        layout.addWidget(table_title)

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

    def _select_custom_range(self):
        start = self.start_edit.date().toPyDate()
        end = self.end_edit.date().toPyDate()
        if start > end:
            start, end = end, start
        self._set_range(start, end)

    def _set_range(self, start: date, end: date):
        self.current_start = start
        self.current_end = end
        self.start_edit.setDate(QDate(start.year, start.month, start.day))
        self.end_edit.setDate(QDate(end.year, end.month, end.day))
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
