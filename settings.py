"""
用户设置持久化。
"""
import json
import os


SETTINGS_PATH = os.path.expanduser("~/.config/keymouse-stats/settings.json")
DEFAULT_SETTINGS = {
    "theme": "light",
    "notifications_enabled": True,
    "notification_threshold": 1880,
}


def _ensure_dir():
    settings_dir = os.path.dirname(SETTINGS_PATH)
    if settings_dir and not os.path.exists(settings_dir):
        os.makedirs(settings_dir, exist_ok=True)


def load_settings() -> dict:
    """读取用户设置，文件不存在或损坏时使用默认值。"""
    if not os.path.exists(SETTINGS_PATH):
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT_SETTINGS)

    settings = dict(DEFAULT_SETTINGS)
    if isinstance(data, dict):
        settings.update(data)
    return settings


def save_settings(settings: dict):
    """保存用户设置。"""
    _ensure_dir()
    merged = dict(DEFAULT_SETTINGS)
    merged.update(settings or {})
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)


def get_theme() -> str:
    """获取当前主题名。"""
    return load_settings().get("theme", DEFAULT_SETTINGS["theme"])


def set_theme(theme_name: str):
    """设置并保存当前主题名。"""
    settings = load_settings()
    settings["theme"] = theme_name
    save_settings(settings)


def get_notifications_enabled() -> bool:
    """获取是否启用通知提醒。"""
    return bool(load_settings().get("notifications_enabled", True))


def get_notification_threshold() -> int:
    """获取通知提醒阈值。"""
    try:
        threshold = int(load_settings().get("notification_threshold", 1880))
    except (TypeError, ValueError):
        threshold = 1880
    return max(1, threshold)


def set_notification_settings(enabled: bool, threshold: int):
    """设置并保存通知提醒配置。"""
    current = load_settings()
    current["notifications_enabled"] = bool(enabled)
    current["notification_threshold"] = max(1, int(threshold))
    save_settings(current)
