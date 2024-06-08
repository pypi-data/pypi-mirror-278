from abc import ABC, abstractmethod


class DataConnector(ABC):

    @abstractmethod
    def read_data(self):
        """
        Read data from the source.
        """
        pass

    @abstractmethod
    def write_data(self, data):
        """
        Write data to the source.
        """
        pass

    @abstractmethod
    def connector_type(self):
        """
        Return the type of the connector.
        """
        pass
