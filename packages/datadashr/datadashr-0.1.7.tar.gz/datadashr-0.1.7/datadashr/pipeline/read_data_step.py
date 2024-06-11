from datadashr.pipeline.data_step import DataStep
from datadashr.config import *


class ReadDataStep(DataStep):
    def execute(self, context):
        """
        Execute the read data step
        :param context:
        :return:
        """
        try:
            data_connector = context.get('data_connector')
            context['df'] = data_connector.read_data()
            if context.get('verbose'):
                logger.info(f"{self.name}: Data read successfully")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: Error reading data: {e}")
            context['df'] = None
            return
