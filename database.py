"""
数据库模块 - SQLite操作
"""
import sqlite3
import os
from datetime import date, datetime
from typing import Optional, Dict, List
import config


class Database:
    """数据库管理类"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DB_PATH
        self._ensure_dir()
        self._init_db()

    def _ensure_dir(self):
        """确保数据库目录存在"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def _init_db(self):
        """初始化数据库表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE UNIQUE NOT NULL,
                    key_presses INTEGER DEFAULT 0,
                    mouse_left_clicks INTEGER DEFAULT 0,
                    mouse_right_clicks INTEGER DEFAULT 0,
                    mouse_move_distance REAL DEFAULT 0.0,
                    scroll_distance INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS key_detail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    key_name TEXT NOT NULL,
                    press_count INTEGER DEFAULT 0,
                    UNIQUE(date, key_name)
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_key_detail_date
                ON key_detail(date)
            """)
            conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_today_stats(self) -> Dict:
        """获取今日统计数据"""
        today = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM daily_stats WHERE date = ?",
                (today,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            else:
                # 创建今日记录
                return self._create_today_record()

    def _create_today_record(self) -> Dict:
        """创建今日统计记录"""
        today = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO daily_stats (date) VALUES (?)
            """, (today,))
            conn.commit()
            return {
                'date': today,
                'key_presses': 0,
                'mouse_left_clicks': 0,
                'mouse_right_clicks': 0,
                'mouse_move_distance': 0.0,
                'scroll_distance': 0
            }

    def update_stats(self, **kwargs):
        """更新今日统计数据"""
        today = date.today().isoformat()
        fields = []
        values = []

        for key, value in kwargs.items():
            if value and key in ['key_presses', 'mouse_left_clicks',
                                   'mouse_right_clicks', 'scroll_distance']:
                fields.append(f"{key} = {key} + ?")
                values.append(value)
            elif value and key == 'mouse_move_distance':
                fields.append("mouse_move_distance = mouse_move_distance + ?")
                values.append(value)

        if not fields:
            return

        values.append(today)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE daily_stats
                SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE date = ?
            """, values)
            conn.commit()

    def reset_today_stats(self):
        """重置今日统计数据"""
        today = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE daily_stats
                SET key_presses = 0,
                    mouse_left_clicks = 0,
                    mouse_right_clicks = 0,
                    mouse_move_distance = 0.0,
                    scroll_distance = 0,
                    updated_at = CURRENT_TIMESTAMP
                WHERE date = ?
            """, (today,))
            conn.commit()

    def get_history(self, days: int = 7) -> List[Dict]:
        """获取历史统计记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM daily_stats
                ORDER BY date DESC
                LIMIT ?
            """, (days,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_stats_by_date_range(self, start_date: str, end_date: str) -> Dict:
        """获取日期范围内的汇总统计"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    COALESCE(SUM(key_presses), 0) AS key_presses,
                    COALESCE(SUM(mouse_left_clicks), 0) AS mouse_left_clicks,
                    COALESCE(SUM(mouse_right_clicks), 0) AS mouse_right_clicks,
                    COALESCE(SUM(mouse_move_distance), 0.0) AS mouse_move_distance,
                    COALESCE(SUM(scroll_distance), 0) AS scroll_distance
                FROM daily_stats
                WHERE date BETWEEN ? AND ?
            """, (start_date, end_date))
            row = cursor.fetchone()
            result = dict(row) if row else {}
            result['total_clicks'] = (
                result.get('mouse_left_clicks', 0) +
                result.get('mouse_right_clicks', 0)
            )
            return result

    def get_daily_stats_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """获取日期范围内每日明细"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM daily_stats
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC
            """, (start_date, end_date))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_key_stats_by_date_range(self, start_date: str, end_date: str) -> Dict:
        """获取日期范围内按键热力统计"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT key_name, COALESCE(SUM(press_count), 0) AS press_count
                FROM key_detail
                WHERE date BETWEEN ? AND ?
                GROUP BY key_name
            """, (start_date, end_date))
            rows = cursor.fetchall()
            return {row['key_name']: row['press_count'] for row in rows}

    def get_date_bounds(self) -> Dict:
        """获取数据库中已有记录的最早和最晚日期。"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT MIN(date) AS start_date, MAX(date) AS end_date
                FROM daily_stats
            """)
            row = cursor.fetchone()
            return dict(row) if row else {'start_date': None, 'end_date': None}

    def ensure_today_record(self):
        """确保今日记录存在"""
        self.get_today_stats()

    def update_key_stats(self, key_name, count=1):
        """更新单个按键的今日计数"""
        today = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO key_detail (date, key_name, press_count)
                VALUES (?, ?, ?)
                ON CONFLICT(date, key_name) DO UPDATE SET
                    press_count = press_count + ?
            """, (today, key_name, count, count))
            conn.commit()

    def flush_key_stats(self, stats_dict):
        """批量写入按键统计数据"""
        if not stats_dict:
            return
        today = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for key_name, count in stats_dict.items():
                if count <= 0:
                    continue
                cursor.execute("""
                    INSERT INTO key_detail (date, key_name, press_count)
                    VALUES (?, ?, ?)
                    ON CONFLICT(date, key_name) DO UPDATE SET
                        press_count = press_count + ?
                """, (today, key_name, count, count))
            conn.commit()

    def get_today_key_stats(self):
        """获取今日按键详细统计"""
        today = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT key_name, press_count FROM key_detail WHERE date = ?",
                (today,)
            )
            rows = cursor.fetchall()
            return {row['key_name']: row['press_count'] for row in rows}

    def reset_today_key_stats(self):
        """重置今日按键详细统计"""
        today = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM key_detail WHERE date = ?",
                (today,)
            )
            conn.commit()

    def close(self):
        """关闭数据库连接"""
        pass  # SQLite连接会在上下文管理器退出时自动关闭
