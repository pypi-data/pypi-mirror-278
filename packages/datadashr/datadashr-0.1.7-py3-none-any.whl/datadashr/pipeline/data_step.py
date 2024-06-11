from datadashr.config import *


class DataStep:
    def __init__(self, name):
        """
        Constructor for DataStep
        :param name:
        """
        self.name = name

    def execute(self, context):
        """
        Execute the data step
        :param context:
        :return:
        """
        raise NotImplementedError("Each step must implement the execute method")
