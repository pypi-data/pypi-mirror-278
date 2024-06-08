import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class ResponseFormatter:
    def __init__(self, result, full_code, connector_type, df_columns, query):
        self.result = result
        self.full_code = full_code
        self.connector_type = connector_type
        self.df_columns = df_columns
        self.query = query

    def format(self, format_type):
        if format_type == 'api':
            return self._format_api()
        elif format_type == 'data':
            return self._format_data()
        elif format_type == 'streamlit':
            return self._format_streamlit()
        elif format_type == 'rich':
            return self._format_rich()
        elif format_type == 'panel':
            return self._format_panel()
        else:
            raise ValueError(f"Unknown format type: {format_type}")

    def _format_api(self):
        if isinstance(self.result, pd.DataFrame):
            return {
                "result": self.result.to_dict(orient='records'),
                "full_code": self.full_code,
                "connector_type": self.connector_type,
                "df_columns": self.df_columns,
                "response_type": "dataframe",
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

    def _format_data(self):
        if isinstance(self.result, pd.DataFrame):
            return self.result
        elif self.result is not None:
            return self.result
        else:
            return None

    def _format_streamlit(self):
        if isinstance(self.result, pd.DataFrame):
            import streamlit as st
            st.dataframe(self.result)
            return self.result
        elif self.result is not None:
            import streamlit as st
            st.text(self.result)
            return self.result
        else:
            return None

    def _format_rich(self):
        console = Console()
        if isinstance(self.result, pd.DataFrame):
            table = Table(show_header=True, header_style="bold magenta")
            for column in self.result.columns:
                table.add_column(column, min_width=10, max_width=40)
            for _, row in self.result.iterrows():
                table.add_row(*map(str, row.values))
            console.print(table)
        elif self.result is not None:
            console.print(Panel(Text(str(self.result)), title="Response", style="bold green"))
        else:
            console.print(Panel("No result available.", title="Response", style="bold red"))
        return None

    def _format_panel(self):
        if isinstance(self.result, pd.DataFrame):
            # Handling NaN values before converting to dictionary
            result_dict = self.result.fillna('NaN').to_dict(orient='records')
            return {
                "result": result_dict,
                "full_code": self.full_code,
                "connector_type": self.connector_type,
                "df_columns": self.df_columns,
                "response_type": "dataframe",
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
