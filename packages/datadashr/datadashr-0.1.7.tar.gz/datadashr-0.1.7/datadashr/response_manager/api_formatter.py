import pandas as pd
from datadashr.response_manager.base import ResponseFormatterBase
from datadashr.config import *


class ApiResponseFormatter(ResponseFormatterBase):
    def format(self):
        try:
            if isinstance(self.result, pd.DataFrame):
                return {
                    "result": self.result.to_dict(orient='records'),
                    "full_code": self.full_code,
                    "connector_type": self.connector_type,
                    "df_columns": self.df_columns,
                    "response_type": "dataframe",
                    "query": self.query,
                }
            elif isinstance(self.result, dict):
                return {
                    "result": self.result,
                    "full_code": self.full_code,
                    "connector_type": self.connector_type,
                    "df_columns": self.df_columns,
                    "response_type": "chart",
                    "query": self.query,
                }
            elif self.result is not None:
                return {
                    "result": self.result,
                    "full_code": self.full_code,
                    "connector_type": self.connector_type,
                    "df_columns": self.df_columns,
                    "response_type": "text",
                    "query": self.query
                }
            else:
                return {
                    "result": None,
                    "full_code": self.full_code,
                    "connector_type": self.connector_type,
                    "df_columns": self.df_columns,
                    "response_type": "none",
                    "query": self.query,
                }
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return {
                "result": None,
                "full_code": self.full_code,
                "connector_type": self.connector_type,
                "df_columns": self.df_columns,
                "response_type": "none",
                "query": self.query,
            }
