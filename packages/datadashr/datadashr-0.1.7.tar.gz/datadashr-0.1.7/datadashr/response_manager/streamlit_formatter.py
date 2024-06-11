import streamlit as st
import pandas as pd
from datadashr.response_manager.base import ResponseFormatterBase
from datadashr.config import *


class StreamlitResponseFormatter(ResponseFormatterBase):
    def format(self):
        """
        Format the response for Streamlit
        :return:
        """
        if isinstance(self.result, pd.DataFrame):
            st.dataframe(self.result)
            return self.result
        elif isinstance(self.result, dict):
            chart_image = self.generate_chart_from_response(self.result)
            st.image(chart_image)
            return chart_image
        elif self.result is not None:
            st.text(self.result)
            return self.result
        else:
            return None
