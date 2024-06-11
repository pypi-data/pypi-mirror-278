from datadashr.pipeline.data_step import DataStep
from datadashr.response_manager import ResponseFormatter
from datadashr.config import *


class FormatResponseStep(DataStep):
    def execute(self, context):
        """
        Execute the response formatting step
        :param context: 
        :return: 
        """
        try:
            self._extracted_from_execute(context)
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: Error formatting response: {e}")
            context['formatted_response'] = {
                "result": None,
                "full_code": context.get('sandbox_response').get('full_code'),
                "connector_type": context.get('data_connector_type'),
                "df_columns": context['df'].columns.tolist(),
                "response_type": "none",
                "query": context['request'],
            }
            if context.get('verbose'):
                logger.info(f"Context after formatting error: {context}")

    def _extracted_from_execute(self, context):
        """
        Extracted from execute
        :param context:
        :return:
        """
        try:
            result = context.get('sandbox_response').get('result')
            if context.get('verbose'):
                logger.info(f"{self.name}: Formatting result {result}")
            full_code = context.get('sandbox_response').get('full_code')
            if context.get('verbose'):
                logger.info(f"{self.name}: Full code {full_code}")
            formatter = ResponseFormatter(result, full_code, context.get('data_connector_type'),
                                          context['df'].columns.tolist(), context['request'], context.get('chart_dir'))
            if context.get('verbose'):
                logger.info(f"{self.name}: Formatting type {context.get('format_type', 'api')}")
            formatted_response = formatter.format(context.get('format_type', 'api'))
            if context.get('verbose'):
                logger.info(f"{self.name}: Formatted response {formatted_response}")
            context['formatted_response'] = formatted_response
            if context.get('verbose'):
                logger.info(f"{self.name}: Response formatting completed")
                logger.info(f"Context after formatting: {context}")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: Error formatting response: {e}")
            context['formatted_response'] = {
                "result": None,
                "full_code": context.get('sandbox_response').get('full_code'),
                "connector_type": context.get('data_connector_type'),
                "df_columns": context['df'].columns.tolist(),
                "response_type": "none",
                "query": context['request'],
            }
            if context.get('verbose'):
                logger.info(f"Context after formatting error: {context}")
