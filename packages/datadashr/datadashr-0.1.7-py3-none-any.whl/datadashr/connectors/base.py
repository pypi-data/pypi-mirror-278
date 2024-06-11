from abc import ABC, abstractmethod
from datadashr.config import *


class DataConnector(ABC):
    """
    Abstract base class for data connectors.

    Methods:
    - read_data: Read data from the source.
    - write_data: Write data to the source.
    - connector_type: Return the type of the connector.
    """


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
