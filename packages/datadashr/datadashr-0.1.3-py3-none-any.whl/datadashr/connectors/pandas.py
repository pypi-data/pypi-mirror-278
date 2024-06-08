import pandas as pd
from datadashr.connectors.base import DataConnector


class CSVConnector(DataConnector):
    def __init__(self, filepath):
        self.filepath = filepath
        self.connector_type = 'pandas'

    def read_data(self):
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
        return self.connector_type

    def write_data(self, data):
        data.to_csv(self.filepath, index=False)
