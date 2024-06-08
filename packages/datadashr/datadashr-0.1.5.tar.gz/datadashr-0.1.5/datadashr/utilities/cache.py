import sqlite3
import json
from datetime import datetime, timedelta
from datadashr.utilities import Utilities
from loguru import logger


class CacheManager:

    def __init__(self, db_folder, verbose=False):
        self.db_folder = db_folder
        self.db_file = f"{db_folder}/cache.db"
        self.verbose = verbose
        self.ut = Utilities(self.verbose)
        self._create_cache_table()

    def _create_cache_table(self):
        """
        
        :return:
        """
        if self.verbose:
            logger.info("Creating cache table if not exists")
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cache (
                        key TEXT PRIMARY KEY,
                        prompt TEXT,
                        code TEXT,
                        timestamp DATETIME
                    )
                ''')
                conn.commit()
        except Exception as e:
            logger.error(f"Error creating cache table: {e}")

    def _generate_key(self, request, columns):
        try:
            columns_str = json.dumps(columns, sort_keys=True)
            return f"{request}-{columns_str}"
        except Exception as e:
            if self.verbose:
                logger.error(f"Error generating key: {e}")
            return None

    def get(self, request, columns):
        try:
            self.clean_old_entries()
            key = self._generate_key(request, columns)
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT prompt, code FROM cache WHERE key = ?', (key,))
                if result := cursor.fetchone():
                    return {'prompt': result[0], 'code': result[1]}
                return None
        except Exception as e:
            if self.verbose:
                logger.error(f"Error getting cache: {e}")
            return None

    def set(self, request, columns, value):
        try:
            key = self._generate_key(request, columns)
            timestamp = datetime.now()
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO cache (key, prompt, code, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (key, json.dumps(value['prompt']), value['code'], timestamp))
                conn.commit()
        except Exception as e:
            logger.error(f"Error setting cache: {e}")

    def clean_old_entries(self):
        try:
            threshold = datetime.now() - timedelta(days=30)
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM cache WHERE timestamp < ?', (threshold,))
                conn.commit()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error cleaning cache: {e}")

    def clean_cache(self):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM cache')
                conn.commit()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error cleaning cache: {e}")
