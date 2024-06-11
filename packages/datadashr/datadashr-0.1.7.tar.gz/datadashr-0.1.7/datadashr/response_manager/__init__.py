from datadashr.response_manager.data_formatter import DataResponseFormatter
from datadashr.response_manager.api_formatter import ApiResponseFormatter
from datadashr.response_manager.panel_formatter import PanelResponseFormatter
from datadashr.response_manager.streamlit_formatter import StreamlitResponseFormatter
from datadashr.config import *


class ResponseFormatter:
    def __init__(self, result, full_code, connector_type, df_columns, query, chart_dir=None):
        self.result = result
        self.full_code = full_code
        self.connector_type = connector_type
        self.df_columns = df_columns
        self.query = query
        self.chart_dir = chart_dir

    def format(self, format_type):
        """
        Format the response
        :param format_type:
        :return:
        """
        try:
            if format_type == 'api':
                """
                Format the response for API
                """
                return ApiResponseFormatter(self.result, self.full_code, self.connector_type, self.df_columns,
                                            self.query).format()
            elif format_type == 'data':
                """
                Format the response for Data
                """
                return DataResponseFormatter(self.result, self.full_code, self.connector_type, self.df_columns,
                                             self.query).format()
            elif format_type == 'streamlit':
                """
                Format the response for Streamlit
                """
                return StreamlitResponseFormatter(self.result, self.full_code, self.connector_type, self.df_columns,
                                                  self.query).format()
            elif format_type == 'panel':
                """
                Format the response for Panel
                """
                return PanelResponseFormatter(self.result, self.full_code, self.connector_type, self.df_columns,
                                              self.query, self.chart_dir).format()
            else:
                raise ValueError(f"Unknown format type: {format_type}")
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

