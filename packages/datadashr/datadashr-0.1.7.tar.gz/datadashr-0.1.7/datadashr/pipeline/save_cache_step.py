from datadashr.pipeline.data_step import DataStep
from datadashr.config import *


class SaveCacheStep(DataStep):
    def execute(self, context):
        """
        Execute the save cache step
        :param context:
        :return:
        """
        try:
            request = context.get('request')
            if context.get('enable_cache'):
                cache_manager = context.get('cache_manager')
                cache_manager.set(request, list(context['df'].columns), {
                    'prompt': context['request'],
                    'code': context['sandbox_response']['full_code']
                })
                if context.get('verbose'):
                    logger.info(f"{self.name}: Cache saved for request")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during cache saving: {e}")
            return
