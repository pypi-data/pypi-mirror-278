from datadashr.pipeline.data_step import DataStep
from datadashr.config import *


class CacheStep(DataStep):
    def execute(self, context):
        """
        Execute the cache step
        :param context:
        :return:
        """
        try:
            request = context.get('request')
            if context.get('enable_cache'):
                cache_manager = context.get('cache_manager')
                if cached_result := cache_manager.get(
                        request, list(context['df'].columns)
                ):
                    context['cached_result'] = cached_result
                    context['llm_response'] = cached_result['code']
                    context['skip_prompt_generation'] = True
                    if context.get('verbose'):
                        logger.info(f"{self.name}: Cache hit for request")
                else:
                    context['cached_result'] = None
                    if context.get('verbose'):
                        logger.info(f"{self.name}: No cache hit for request")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during cache step: {e}")
            context['cached_result'] = None
            context['llm_response'] = None
            context['skip_prompt_generation'] = False
            return
