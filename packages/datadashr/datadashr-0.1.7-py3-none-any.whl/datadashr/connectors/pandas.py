import pandas as pd
from datadashr.connectors.base import DataConnector
from datadashr.config import *


class CSVConnector(DataConnector):
    def __init__(self, filepath):
        """
            Initializes a Pandas data connector with the given filepath.

            Args:
            - filepath: The path to the data file.

            Returns:
            - None
            """
        self.filepath = filepath
        self.connector_type = 'pandas'

    def read_data(self):
        """
            Reads data from the CSV file specified by the filepath, preprocesses the data, and returns a Pandas DataFrame.

            Args:
            - None

            Returns:
            - Pandas DataFrame: The preprocessed data read from the CSV file.
            """
        df = pd.read_csv(self.filepath)

        # Convertire i nomi delle colonne in minuscolo
        df.columns = [col.lower() for col in df.columns]

        # Rimuovere spazi vuoti dai nomi delle colonne
        df.columns = [col.strip() for col in df.columns]

        # Sostituire gli spazi negli intestazioni delle colonne con underscore
        df.columns = [col.replace(' ', '_') for col in df.columns]

        # Rimuovere spazi bianchi dai valori delle celle di tipo stringa
        str_cols = df.select_dtypes(include=['object']).columns
        df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

        return df

    def connector_type(self):
        """
            Returns the type of the connector.

            Args:
            - None

            Returns:
            - str: The type of the connector.
            """
        return self.connector_type

    def write_data(self, data):
        """
            Writes the given Pandas DataFrame to the CSV file specified by the filepath.

            Args:
            - data: The Pandas DataFrame to write to the CSV file.

            Returns:
            - None
            """
        data.to_csv(self.filepath, index=False)
