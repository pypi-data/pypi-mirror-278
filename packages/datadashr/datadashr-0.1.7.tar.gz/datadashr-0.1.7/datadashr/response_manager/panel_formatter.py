import panel as pn
import pandas as pd
from datadashr.response_manager.base import ResponseFormatterBase
from io import StringIO
from datadashr.config import *


class PanelResponseFormatter(ResponseFormatterBase):
    def format(self):
        """
        Format the response for Panel
        :return:
        """
        try:
            if isinstance(self.result, pd.DataFrame):
                return pn.widgets.DataFrame(self.result)
            elif isinstance(self.result, dict):
                return self.generate_echart_from_response(self.result)
            elif self.result is not None:
                return pn.pane.Markdown(str(self.result))
            else:
                return pn.pane.Markdown("No result available.")
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return pn.pane.Markdown("Error formatting response.")

    #TODO: manage chart visualization error
    def generate_echart_from_response(self, response):
        """
        Generate an EChart from the response
        :param response:
        :return:
        """
        try:
            if isinstance(response['data'], list):
                data = pd.DataFrame(response['data'])
            elif isinstance(response['data'], dict):
                data = pd.DataFrame(list(response['data'].items()), columns=[response['x_label'], response['y_label']])
            else:
                data = pd.read_json(StringIO(response['data']))

            # Verifica che le colonne esistano
            if response['x_label'] not in data.columns or response['y_label'] not in data.columns:
                raise KeyError(f"Columns {response['x_label']} or {response['y_label']} not found in data")

            echart_data = {
                'title': {'text': 'Chart'},
                'tooltip': {},
                'legend': {'data': [response['y_label']]},
                'xAxis': {'data': data[response['x_label']].tolist()},
                'yAxis': {},
                'series': [{
                    'name': response['y_label'],
                    'type': response['chart_type'],
                    'data': data[response['y_label']].tolist()
                }]
            }

            return pn.pane.ECharts(echart_data, height=480, width=640)
        except Exception as e:
            logger.error(f"Error generating EChart: {e}")
            return pn.pane.Markdown("Error generating EChart.")
