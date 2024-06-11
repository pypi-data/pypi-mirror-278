from datadashr.pipeline.data_step import DataStep
from datadashr.config import *


class SaveVectorStep(DataStep):
    def execute(self, context):
        """
        Execute the save vector step
        :param context:
        :return:
        """
        try:
            if context.get('enable_vector'):
                vector_manager = context.get('vector_manager')
                vector_manager.set_vector(context['request'], list(context['df'].columns), {
                    'prompt': context['request'],
                    'code': context['sandbox_response']['full_code']
                })
                if context.get('verbose'):
                    logger.info(f"{self.name}: Vector saved for request")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during vector saving: {e}")
            return
