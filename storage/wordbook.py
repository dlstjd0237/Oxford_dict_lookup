from __future__ import annotations

import os
import sqlite3
import threading
import time
import logging
from typing import Optional

import config
from dictionary.models import WordResult

logger = logging.getLogger(__name__)


class Wordbook:
    def __init__(self):
        db_dir = os.path.dirname(config.CACHE_DB_PATH)
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, 'wordbook.db')
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._lock = threading.Lock()
        self._create_table()

    def _create_table(self):
        with self._lock:
            self._conn.execute('''
                CREATE TABLE IF NOT EXISTS wordbook (
                    word TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    added_at REAL NOT NULL
                )
            ''')
            self._conn.commit()

    def add(self, result: WordResult):
        data_json = result.to_json()
        with self._lock:
            self._conn.execute(
                'INSERT OR REPLACE INTO wordbook (word, data, added_at) VALUES (?, ?, ?)',
                (result.word.lower(), data_json, time.time())
            )
            self._conn.commit()

    def remove(self, word: str):
        with self._lock:
            self._conn.execute('DELETE FROM wordbook WHERE word = ?', (word.lower(),))
            self._conn.commit()

    def contains(self, word: str) -> bool:
        with self._lock:
            row = self._conn.execute(
                'SELECT 1 FROM wordbook WHERE word = ?', (word.lower(),)
            ).fetchone()
        return row is not None

    def get_all(self) -> list[tuple[str, float]]:
        """Return list of (word, added_timestamp) ordered by most recent."""
        with self._lock:
            rows = self._conn.execute(
                'SELECT word, added_at FROM wordbook ORDER BY added_at DESC'
            ).fetchall()
        return rows

    def get_result(self, word: str) -> Optional[WordResult]:
        with self._lock:
            row = self._conn.execute(
                'SELECT data FROM wordbook WHERE word = ?', (word.lower(),)
            ).fetchone()
        if row is None:
            return None
        return WordResult.from_json(row[0])

    def close(self):
        with self._lock:
            self._conn.close()
