from datadashr.config import *


class BaseLLM:
    """
    Base class for all Language Learning Models (LLMs)
    """

    def __init__(self, model, params, verbose=False):
        """
        Constructor for BaseLLM
        :param model:
        :param params:
        """
        self.model = model
        self.params = params
        self.verbose = verbose

    def chat(self, messages):
        """
        Chat with the model
        :param messages:
        :return:
        """
        raise NotImplementedError("This method should be overridden by subclasses")
