"""
键盘热力图渲染组件 - 浅色仪表盘风格
"""
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QToolTip
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QMouseEvent, QLinearGradient
import keyboard_layouts as kl


THEME_COLORS = {
    'light': {'text': '#0F172A', 'muted': '#64748B', 'panel': '#F8FAFC', 'border': '#E2E8F0', 'key': '#FFFFFF', 'key_border': '#D7DEE8', 'hover': '#2563EB', 'chip_bg': '#EFF6FF', 'chip_border': '#DBEAFE', 'chip_text': '#1D4ED8', 'empty_bg': '#FFFFFF'},
    'dark': {'text': '#F8FAFC', 'muted': '#94A3B8', 'panel': '#1E293B', 'border': '#334155', 'key': '#111827', 'key_border': '#475569', 'hover': '#60A5FA', 'chip_bg': '#1E3A8A', 'chip_border': '#2563EB', 'chip_text': '#DBEAFE', 'empty_bg': '#111827'},
    'blue': {'text': '#0F2A43', 'muted': '#52708D', 'panel': '#F0F7FF', 'border': '#CFE4FF', 'key': '#FFFFFF', 'key_border': '#BBD7F5', 'hover': '#1677FF', 'chip_bg': '#E6F4FF', 'chip_border': '#BAE0FF', 'chip_text': '#0958D9', 'empty_bg': '#FFFFFF'},
    'green': {'text': '#052E16', 'muted': '#4B755D', 'panel': '#F0FDF4', 'border': '#BBF7D0', 'key': '#FFFFFF', 'key_border': '#86EFAC', 'hover': '#16A34A', 'chip_bg': '#DCFCE7', 'chip_border': '#86EFAC', 'chip_text': '#166534', 'empty_bg': '#FFFFFF'},
    'mint': {'text': '#123C35', 'muted': '#5B8178', 'panel': '#F2FBF7', 'border': '#C8F0E1', 'key': '#FFFFFF', 'key_border': '#9EE6D0', 'hover': '#14B8A6', 'chip_bg': '#CCFBF1', 'chip_border': '#99F6E4', 'chip_text': '#0F766E', 'empty_bg': '#FFFFFF'},
    'aqua': {'text': '#123A47', 'muted': '#557887', 'panel': '#F0FDFF', 'border': '#BAE6FD', 'key': '#FFFFFF', 'key_border': '#7DD3FC', 'hover': '#0891B2', 'chip_bg': '#CFFAFE', 'chip_border': '#67E8F9', 'chip_text': '#0E7490', 'empty_bg': '#FFFFFF'},
    'lavender': {'text': '#32204D', 'muted': '#74658F', 'panel': '#FAF7FF', 'border': '#E9D5FF', 'key': '#FFFFFF', 'key_border': '#D8B4FE', 'hover': '#8B5CF6', 'chip_bg': '#EDE9FE', 'chip_border': '#DDD6FE', 'chip_text': '#6D28D9', 'empty_bg': '#FFFFFF'},
    'peach': {'text': '#4A2A16', 'muted': '#8A6752', 'panel': '#FFF9F2', 'border': '#FED7AA', 'key': '#FFFFFF', 'key_border': '#FDBA74', 'hover': '#F97316', 'chip_bg': '#FFEDD5', 'chip_border': '#FED7AA', 'chip_text': '#C2410C', 'empty_bg': '#FFFFFF'},
    'cream': {'text': '#3F3718', 'muted': '#7E7350', 'panel': '#FFFDEA', 'border': '#FDE68A', 'key': '#FFFFFF', 'key_border': '#FACC15', 'hover': '#CA8A04', 'chip_bg': '#FEF3C7', 'chip_border': '#FDE68A', 'chip_text': '#92400E', 'empty_bg': '#FFFFFF'},
}


class KeyboardHeatmap(QWidget):
    """键盘热力图，支持 87/104 键布局、Top 按键摘要和图例。"""

    GAP_RATIO = 0.11
    CORNER_RADIUS = 5.0

    HEAT_COLORS = [
        (0.00, QColor('#EEF2F7')),
        (0.06, QColor('#DCFCE7')),
        (0.22, QColor('#86EFAC')),
        (0.46, QColor('#FDE047')),
        (0.70, QColor('#FB923C')),
        (0.90, QColor('#EF4444')),
        (1.00, QColor('#B91C1C')),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout_type = '87'
        self._layout = kl.get_layout_87()
        self._key_stats = {}
        self._max_count = 1
        self._total_presses = 0
        self._range_label = '今日'
        self._key_rects = []
        self._hovered_key = None
        self._theme_name = 'light'
        self._colors = THEME_COLORS['light']

        self.setMouseTracking(True)
        self.setMinimumSize(560, 360)
        self.setStyleSheet('background: transparent;')

        self._init_ui()
        self.set_theme(self._theme_name)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(0)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)

        title_box = QVBoxLayout()
        title_box.setContentsMargins(0, 0, 0, 0)
        title_box.setSpacing(2)

        self.title_label = QLabel('键盘热力图')
        self.title_label.setStyleSheet('font-size: 17px; font-weight: 700; color: #0F172A; background: transparent;')

        self.subtitle_label = QLabel('今日 · 0 次按键')
        self.subtitle_label.setStyleSheet('font-size: 12px; color: #64748B; background: transparent;')

        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)
        toolbar.addLayout(title_box)
        toolbar.addStretch()

        self._btn_87 = QPushButton('87键')
        self._btn_104 = QPushButton('104键')
        for btn in (self._btn_87, self._btn_104):
            btn.setCheckable(True)
            btn.setFixedSize(54, 26)
        self._btn_87.setChecked(True)
        self._btn_87.clicked.connect(lambda: self._switch_layout('87'))
        self._btn_104.clicked.connect(lambda: self._switch_layout('104'))

        toolbar.addWidget(self._btn_87)
        toolbar.addWidget(self._btn_104)
        layout.addLayout(toolbar)
        layout.addStretch()

    def set_theme(self, theme_name: str):
        self._theme_name = theme_name if theme_name in THEME_COLORS else 'light'
        self._colors = THEME_COLORS[self._theme_name]
        self.title_label.setStyleSheet(
            f"font-size: 17px; font-weight: 700; color: {self._colors['text']}; background: transparent;"
        )
        self.subtitle_label.setStyleSheet(
            f"font-size: 12px; color: {self._colors['muted']}; background: transparent;"
        )
        self.update()

    def _switch_layout(self, layout_type: str):
        self._layout_type = layout_type
        self._layout = kl.get_layout_104() if layout_type == '104' else kl.get_layout_87()
        self._btn_87.setChecked(layout_type == '87')
        self._btn_104.setChecked(layout_type == '104')
        self.update()

    def set_key_stats(self, stats: dict[str, int]):
        self._key_stats = {str(k).lower(): int(v) for k, v in stats.items() if int(v) > 0}
        self._max_count = max(self._key_stats.values()) if self._key_stats else 1
        self.update()

    def set_context(self, range_label: str, total_presses: int):
        self._range_label = range_label
        self._total_presses = int(total_presses or 0)
        self.subtitle_label.setText(f'{self._range_label} · {self._total_presses:,} 次按键')
        self.update()

    def _heat_color(self, count: int) -> QColor:
        if count <= 0 or self._max_count <= 0:
            return self.HEAT_COLORS[0][1]
        ratio = min(count / self._max_count, 1.0)
        for i in range(len(self.HEAT_COLORS) - 1):
            t0, c0 = self.HEAT_COLORS[i]
            t1, c1 = self.HEAT_COLORS[i + 1]
            if ratio <= t1:
                local = (ratio - t0) / (t1 - t0) if t1 > t0 else 0
                return QColor(
                    int(c0.red() + (c1.red() - c0.red()) * local),
                    int(c0.green() + (c1.green() - c0.green()) * local),
                    int(c0.blue() + (c1.blue() - c0.blue()) * local),
                )
        return self.HEAT_COLORS[-1][1]

    def _text_color_for(self, color: QColor, active: bool) -> QColor:
        if not active:
            return QColor(self._colors['text'])
        return QColor('#FFFFFF') if color.lightness() < 128 else QColor('#111827')

    def _key_count(self, key_def: dict) -> int:
        return sum(self._key_stats.get(name.lower(), 0) for name in key_def['key_names'])

    def _display_label(self, key_def: dict) -> str:
        label = key_def.get('label') or ''
        if label:
            return label
        if 'space' in key_def.get('key_names', []):
            return 'Space'
        return key_def['key_names'][0]

    def _keyboard_geometry(self):
        keys = self._layout
        min_row = min(k['row'] for k in keys)
        max_row = max(k['row'] + k.get('height', 1.0) for k in keys)
        min_col = min(k['col'] for k in keys)
        max_col = max(k['col'] + k['width'] for k in keys)

        num_rows = max_row - min_row
        num_cols = max_col - min_col
        margin = 18
        top_offset = 64
        bottom_offset = 138
        paint_w = self.width() - margin * 2
        paint_h = self.height() - top_offset - bottom_offset
        key_unit = min(paint_w / num_cols, paint_h / num_rows)
        total_w = num_cols * key_unit
        total_h = num_rows * key_unit
        start_x = margin + (paint_w - total_w) / 2
        start_y = top_offset + (paint_h - total_h) / 2
        return min_row, min_col, key_unit, QRectF(start_x, start_y, total_w, total_h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._key_rects.clear()

        if not self._layout:
            painter.end()
            return

        min_row, min_col, key_unit, keyboard_rect = self._keyboard_geometry()
        if key_unit <= 0:
            painter.end()
            return

        self._draw_panel_background(painter, keyboard_rect)
        self._draw_keys(painter, min_row, min_col, key_unit, keyboard_rect)
        self._draw_legend(painter)
        self._draw_top_keys(painter)

        if not self._key_stats:
            self._draw_empty_state(painter, keyboard_rect)

        painter.end()

    def _draw_panel_background(self, painter: QPainter, keyboard_rect: QRectF):
        bg = keyboard_rect.adjusted(-12, -12, 12, 12)
        painter.setPen(QPen(QColor(self._colors['border']), 1))
        painter.setBrush(QColor(self._colors['panel']))
        painter.drawRoundedRect(bg, 14, 14)

    def _draw_keys(self, painter: QPainter, min_row: float, min_col: float, key_unit: float, keyboard_rect: QRectF):
        gap = max(1.3, key_unit * self.GAP_RATIO)
        font_size = max(6, min(11, int(key_unit * 0.30)))

        for key_def in self._layout:
            col = key_def['col'] - min_col
            row = key_def['row'] - min_row
            x = keyboard_rect.x() + col * key_unit + gap / 2
            y = keyboard_rect.y() + row * key_unit + gap / 2
            w = key_def['width'] * key_unit - gap
            h = key_def.get('height', 1.0) * key_unit - gap
            rect = QRectF(x, y, w, h)

            count = self._key_count(key_def)
            active = count > 0
            fill = self._heat_color(count)
            key_id = tuple(key_def['key_names'])
            hovered = key_id == self._hovered_key

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 18 if hovered else 10))
            painter.drawRoundedRect(rect.adjusted(0, 1.8, 0, 1.8), self.CORNER_RADIUS, self.CORNER_RADIUS)

            painter.setPen(QPen(QColor(self._colors['border'] if active else self._colors['key_border']), 1))
            painter.setBrush(fill if active else QColor(self._colors['key']))
            painter.drawRoundedRect(rect, self.CORNER_RADIUS, self.CORNER_RADIUS)

            if active:
                inner = rect.adjusted(2, 2, -2, -2)
                painter.setPen(Qt.NoPen)
                painter.setBrush(fill)
                painter.drawRoundedRect(inner, max(2, self.CORNER_RADIUS - 1), max(2, self.CORNER_RADIUS - 1))

            if hovered:
                painter.setPen(QPen(QColor(self._colors['hover']), 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawRoundedRect(rect.adjusted(-1, -1, 1, 1), self.CORNER_RADIUS + 1, self.CORNER_RADIUS + 1)

            label = key_def.get('label', '')
            if label and w > 10 and h > 9:
                font = QFont('Segoe UI', font_size)
                font.setBold(True)
                painter.setFont(font)
                painter.setPen(self._text_color_for(fill, active))
                painter.drawText(rect, Qt.AlignCenter, label)

            self._key_rects.append((rect, key_def, count))

    def _draw_legend(self, painter: QPainter):
        y = self.height() - 50
        x = 18
        w = 210
        h = 9

        painter.setPen(QColor(self._colors['muted']))
        painter.setFont(QFont('Segoe UI', 9))
        painter.drawText(QRectF(x, y - 20, 260, 18), Qt.AlignLeft | Qt.AlignVCenter, '热度图例')

        gradient = QLinearGradient(x, y, x + w, y)
        for pos, color in self.HEAT_COLORS[1:]:
            gradient.setColorAt(pos, color)
        painter.setPen(QPen(QColor(self._colors['border']), 1))
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(QRectF(x, y, w, h), 4, 4)

        painter.setPen(QColor(self._colors['muted']))
        painter.setFont(QFont('Segoe UI', 8))
        painter.drawText(QRectF(x, y + 12, 40, 16), Qt.AlignLeft, '低频')
        painter.drawText(QRectF(x + w - 40, y + 12, 40, 16), Qt.AlignRight, '高频')

    def _draw_top_keys(self, painter: QPainter):
        items = []
        for key_def in self._layout:
            count = self._key_count(key_def)
            if count > 0:
                items.append((self._display_label(key_def), count))
        items.sort(key=lambda x: x[1], reverse=True)
        top = items[:8]

        x = 290
        y = self.height() - 134
        w = self.width() - x - 18
        row_h = 14
        label_w = 78
        value_w = 62
        bar_x = x + label_w
        bar_w = max(80, w - label_w - value_w - 12)

        painter.setPen(QColor(self._colors['muted']))
        painter.setFont(QFont('Segoe UI', 9, QFont.Bold))
        title = '高频按键 Top 8'
        if top:
            max_label, max_count = top[0]
            title = f'{title} · 最高 {max_label} {max_count:,} 次'
        painter.drawText(QRectF(x, y, w, 18), Qt.AlignLeft | Qt.AlignVCenter, title)

        if not top:
            painter.setPen(QColor(self._colors['muted']))
            painter.setFont(QFont('Segoe UI', 9))
            painter.drawText(QRectF(x, y + 24, w, 20), Qt.AlignLeft | Qt.AlignVCenter, '暂无高频按键数据')
            return

        max_count = top[0][1]
        painter.setFont(QFont('Segoe UI', 8))
        for i, (label, count) in enumerate(top):
            row_y = y + 24 + i * row_h
            ratio = count / max_count if max_count else 0

            painter.setPen(QColor(self._colors['text']))
            painter.drawText(QRectF(x, row_y - 1, label_w - 8, row_h), Qt.AlignRight | Qt.AlignVCenter, label)

            bg_rect = QRectF(bar_x, row_y + 4, bar_w, 6)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self._colors['chip_bg']))
            painter.drawRoundedRect(bg_rect, 3, 3)

            fill_rect = QRectF(bar_x, row_y + 4, max(3, bar_w * ratio), 6)
            painter.setBrush(self._heat_color(count))
            painter.drawRoundedRect(fill_rect, 3, 3)

            painter.setPen(QColor(self._colors['muted']))
            painter.drawText(QRectF(bar_x + bar_w + 8, row_y - 1, value_w, row_h), Qt.AlignLeft | Qt.AlignVCenter, f'{count:,}')

    def _draw_empty_state(self, painter: QPainter, keyboard_rect: QRectF):
        box = keyboard_rect.adjusted(40, keyboard_rect.height() * 0.30, -40, -keyboard_rect.height() * 0.30)
        painter.setPen(QPen(QColor(self._colors['border']), 1))
        bg = QColor(self._colors['empty_bg'])
        bg.setAlpha(232)
        painter.setBrush(bg)
        painter.drawRoundedRect(box, 14, 14)
        painter.setPen(QColor(self._colors['muted']))
        painter.setFont(QFont('Segoe UI', 11, QFont.Bold))
        painter.drawText(box, Qt.AlignCenter, '该时间范围暂无按键热力数据')

    def mouseMoveEvent(self, event: QMouseEvent):
        found = None
        for rect, key_def, count in self._key_rects:
            if rect.contains(event.pos()):
                found = tuple(key_def['key_names'])
                label = self._display_label(key_def)
                percent = (count / self._total_presses * 100) if self._total_presses else 0
                QToolTip.showText(
                    event.globalPos(),
                    f'<b>{label}</b><br>今日/范围按下: <b>{count:,}</b> 次<br>占比: {percent:.1f}%'
                )
                break

        if found != self._hovered_key:
            self._hovered_key = found
            self.update()
        if found is None:
            QToolTip.hideText()

    def leaveEvent(self, event):
        self._hovered_key = None
        QToolTip.hideText()
        self.update()
