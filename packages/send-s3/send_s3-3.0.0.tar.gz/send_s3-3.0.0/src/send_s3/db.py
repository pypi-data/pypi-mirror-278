import json
import os
import time
import sqlite3
from datetime import datetime
from typing import Any, Optional

from send_s3.common import app_directory


class Database:
    def __init__(self):
        path = app_directory("log.sqlite3")
        schema_sql = os.path.join(os.path.dirname(__file__), "schema.sql")
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        with open(schema_sql, "r") as f:
            self.cursor.executescript(f.read())

    def insert(self, filepath: str, key: str, size: int, checksum: str, url: str, data: Any) -> Optional[int]:
        date = int(time.time())
        data_json = json.dumps(data)
        self.cursor.execute(
            'INSERT INTO logs (timestamp, filepath, key, size, checksum, url, data) VALUES (?, ?, ?, ?, ?, ?, ?)',
            tuple([date, filepath, key, size, checksum, url, data_json])
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def select(self, limit: int = 100, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None,
               path: Optional[str] = None):
        date_from = int(date_from.timestamp()) if date_from else 0
        date_to = int(date_to.timestamp()) if date_to else (int(time.time()) + 0xffffffff)
        query = 'SELECT timestamp, filepath, key, size, checksum, url, data FROM logs ' \
                'WHERE timestamp >= ? AND timestamp <= ?'
        query_params = [date_from, date_to]
        if path is not None:
            query += ' AND filepath LIKE ?'
            query_params.append(f"%{path}%")
        query += ' ORDER BY timestamp DESC LIMIT ?'
        query_params.append(limit)
        self.cursor.execute(query, tuple(query_params))
        for timestamp, filepath, key, size, checksum, url, data in self.cursor.fetchall():
            yield {
                'timestamp': timestamp,
                'filepath': filepath,
                'key': key,
                'size': size,
                'checksum': checksum,
                'url': url,
                'data': json.loads(data)
            }

    def close(self):
        self.connection.close()

    def __del__(self):
        self.close()
