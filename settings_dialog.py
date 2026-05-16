"""
设置窗口。
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QCheckBox, QSpinBox, QPushButton, QFrame
)
from PyQt5.QtCore import Qt

import settings


THEME_OPTIONS = {
    'light': '浅色',
    'dark': '深色',
    'blue': '蓝色',
    'green': '绿色',
}


class SettingsDialog(QDialog):
    """应用设置对话框。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('设置')
        self.setModal(True)
        self.setFixedSize(360, 240)

        self._init_ui()
        self._load_current_settings()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        title = QLabel('应用设置')
        title.setStyleSheet('font-size: 18px; font-weight: 800;')
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)

        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel('主题'))
        theme_row.addStretch()
        self.theme_combo = QComboBox()
        self.theme_combo.setFixedWidth(150)
        for key, label in THEME_OPTIONS.items():
            self.theme_combo.addItem(label, key)
        theme_row.addWidget(self.theme_combo)
        layout.addLayout(theme_row)

        self.notify_checkbox = QCheckBox('启用键盘敲击提醒')
        layout.addWidget(self.notify_checkbox)

        threshold_row = QHBoxLayout()
        threshold_row.addWidget(QLabel('每增加'))
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(1, 1000000)
        self.threshold_spin.setSingleStep(100)
        self.threshold_spin.setFixedWidth(120)
        threshold_row.addWidget(self.threshold_spin)
        threshold_row.addWidget(QLabel('次提醒'))
        threshold_row.addStretch()
        layout.addLayout(threshold_row)

        layout.addStretch()

        actions = QHBoxLayout()
        actions.addStretch()
        cancel_btn = QPushButton('取消')
        save_btn = QPushButton('保存')
        save_btn.setDefault(True)
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self._save_and_accept)
        actions.addWidget(cancel_btn)
        actions.addWidget(save_btn)
        layout.addLayout(actions)

    def _load_current_settings(self):
        theme = settings.get_theme()
        idx = self.theme_combo.findData(theme)
        self.theme_combo.setCurrentIndex(max(0, idx))
        self.notify_checkbox.setChecked(settings.get_notifications_enabled())
        self.threshold_spin.setValue(settings.get_notification_threshold())

    def _save_and_accept(self):
        settings.set_theme(self.theme_combo.currentData() or 'light')
        settings.set_notification_settings(
            self.notify_checkbox.isChecked(),
            self.threshold_spin.value()
        )
        self.accept()

    def selected_theme(self) -> str:
        return self.theme_combo.currentData() or 'light'

    def notifications_enabled(self) -> bool:
        return self.notify_checkbox.isChecked()

    def notification_threshold(self) -> int:
        return self.threshold_spin.value()
