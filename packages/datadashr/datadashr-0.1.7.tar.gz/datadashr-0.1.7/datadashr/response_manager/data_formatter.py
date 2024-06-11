import pandas as pd
from datadashr.response_manager.base import ResponseFormatterBase
from datadashr.config import *

class DataResponseFormatter(ResponseFormatterBase):
    def format(self):
        """
        Format the response for Data
        :return:
        """
        try:
            if isinstance(self.result, pd.DataFrame):
                return self.result
            elif isinstance(self.result, dict):
                return self.generate_chart_from_response(self.result)
            elif self.result is not None:
                return self.result
            else:
                return None
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return None
