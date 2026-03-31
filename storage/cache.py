import os
import sqlite3
import threading
import time
import logging
from typing import Optional

import config
from dictionary.models import WordResult

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self):
        db_path = config.CACHE_DB_PATH
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._lock = threading.Lock()
        self._create_table()

    def _create_table(self):
        with self._lock:
            self._conn.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    word TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
            ''')
            self._conn.commit()

    def get(self, word: str) -> Optional[WordResult]:
        with self._lock:
            row = self._conn.execute(
                'SELECT data, created_at FROM cache WHERE word = ?', (word,)
            ).fetchone()
            if row is None:
                return None
            data_json, created_at = row
            age_days = (time.time() - created_at) / 86400
            if age_days > config.CACHE_TTL_DAYS:
                self._conn.execute('DELETE FROM cache WHERE word = ?', (word,))
                self._conn.commit()
                return None
        return WordResult.from_json(data_json)

    def put(self, result: WordResult):
        data_json = result.to_json()
        with self._lock:
            self._conn.execute(
                'INSERT OR REPLACE INTO cache (word, data, created_at) VALUES (?, ?, ?)',
                (result.word.lower(), data_json, time.time())
            )
            self._conn.commit()

    def close(self):
        with self._lock:
            self._conn.close()
