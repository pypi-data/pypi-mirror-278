import pandas as pd
import matplotlib.pyplot as plt
import io
import panel as pn
from PIL import Image
from io import StringIO
from datadashr.config import *


class ResponseFormatterBase:
    def __init__(self, result, full_code, connector_type, df_columns, query, chart_dir=None):
        self.result = result
        self.full_code = full_code
        self.connector_type = connector_type
        self.df_columns = df_columns
        self.query = query
        self.chart_dir = chart_dir

    def format(self):
        """
        Format the response
        :return:
        """
        raise NotImplementedError("Subclasses should implement this method")

    def generate_chart_from_response(self, response):
        """
        Generate a chart from the response
        :param response:
        :return:
        """
        try:
            if isinstance(response['data'], list):
                # Caso in cui i dati sono forniti come una lista di dizionari
                data = pd.DataFrame(response['data'])
            elif isinstance(response['data'], dict):
                # Caso in cui i dati sono forniti come un dizionario con indici
                data = pd.DataFrame(list(response['data'].items()), columns=[response['x_label'], response['y_label']])
            else:
                # Caso in cui i dati sono forniti come JSON
                data = pd.read_json(StringIO(response['data']))

            # Verifica che le colonne esistano
            if response['x_label'] not in data.columns or response['y_label'] not in data.columns:
                raise KeyError(f"Columns {response['x_label']} or {response['y_label']} not found in data")

            fig, ax = plt.subplots()

            if response["chart_type"] == "bar":
                ax.bar(data[response["x_label"]], data[response["y_label"]])
                ax.set_xlabel(response["x_label"])
                ax.set_ylabel(response["y_label"])
                for i in range(len(data)):
                    ax.text(i, data[response["y_label"]].iloc[i] / 2, f'{data[response["y_label"]].iloc[i]:.2f}',
                            ha='center', va='center')
            elif response["chart_type"] == "line":
                ax.plot(data[response["x_label"]], data[response["y_label"]])
                ax.set_xlabel(response["x_label"])
                ax.set_ylabel(response["y_label"])
            elif response["chart_type"] == "histogram":
                ax.hist(data[response["y_label"]], bins=10)
                ax.set_xlabel(response["y_label"])
                ax.set_ylabel('Frequency')
            else:
                ax.text(0.5, 0.5, 'No valid chart type specified', horizontalalignment='center', verticalalignment='center')

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)

            if self.chart_dir:
                img.save(self.chart_dir)
                print(f"Image saved to {self.chart_dir}")

            return self.chart_dir or img
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            return None

    def generate_echart_from_response(self, response):
        pass
