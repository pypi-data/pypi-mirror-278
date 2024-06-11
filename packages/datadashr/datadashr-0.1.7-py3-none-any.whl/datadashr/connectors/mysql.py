from datadashr.connectors.base import DataConnector


class SQLConnector(DataConnector):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = self.create_connection()

    def create_connection(self):
        import sqlalchemy
        return sqlalchemy.create_engine(self.connection_string)

    def read_data(self):
        return pd.read_sql_table('table_name', self.connection)

    def write_data(self, data):
        data.to_sql('table_name', self.connection, if_exists='replace', index=False)
