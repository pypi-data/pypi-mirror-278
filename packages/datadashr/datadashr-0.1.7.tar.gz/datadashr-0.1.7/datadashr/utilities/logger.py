import duckdb
import json
from datetime import datetime, timedelta
from loguru import logger


class LogManager:

    def __init__(self, db_path, verbose=False):
        self.db_file = db_path
        self.verbose = verbose
        self._create_logs_table()
        logger.add(self._log_to_db, level="INFO")

    def _create_logs_table(self):
        """
        Create logs table if not exists
        """
        if self.verbose:
            logger.info("Creating logs table if not exists")
        try:
            with duckdb.connect(self.db_file) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS logs (
                        timestamp TIMESTAMP,
                        level TEXT,
                        message TEXT
                    )
                ''')
        except Exception as e:
            logger.error(f"Error creating logs table: {e}")
        """
        Delete old logs
        """
        self.clean_old_logs()

    def _log_to_db(self, message):
        """
        Log handler for Loguru to write logs to DuckDB
        """
        record = message.record
        timestamp = datetime.fromtimestamp(record["time"].timestamp())
        level = record["level"].name
        msg = record["message"]

        try:
            with duckdb.connect(self.db_file) as conn:
                conn.execute('''
                    INSERT INTO logs (timestamp, level, message)
                    VALUES (?, ?, ?)
                ''', (timestamp, level, msg))
        except Exception as e:
            logger.error(f"Error writing log to DB: {e}")

    def get_logs(self, start_date=None, end_date=None, level=None):
        """
        Retrieve logs from DuckDB
        """
        query = "SELECT timestamp, level, message FROM logs WHERE 1=1"
        params = []

        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        if level:
            query += " AND level = ?"
            params.append(level)

        try:
            with duckdb.connect(self.db_file) as conn:
                result = conn.execute(query, params).fetchall()
                logs = [
                    {"timestamp": str(row[0]), "level": row[1], "message": row[2]}
                    for row in result
                ]
                return json.dumps(logs, indent=4)
        except Exception as e:
            logger.error(f"Error retrieving logs: {e}")
            return None

    def clean_old_logs(self, days=30):
        """
        Clean old logs from DuckDB
        """
        threshold = datetime.now() - timedelta(days=days)
        try:
            with duckdb.connect(self.db_file) as conn:
                conn.execute('DELETE FROM logs WHERE timestamp < ?', (threshold,))
        except Exception as e:
            logger.error(f"Error cleaning old logs: {e}")

    def clean_all_logs(self):
        """
        Clean all logs from DuckDB
        """
        try:
            with duckdb.connect(self.db_file) as conn:
                conn.execute('DELETE FROM logs')
        except Exception as e:
            logger.error(f"Error cleaning all logs: {e}")


# Esempio di utilizzo
if __name__ == "__main__":
    log_manager = LogManager("logs", verbose=True)
    logs = log_manager.get_logs()
    print(logs)
