from datadashr.pipeline.data_step import DataStep
from datadashr.config import *


class LLMRequestStep(DataStep):
    def execute(self, context):
        """
        Execute the LLM request step
        :param context:
        :return:
        """
        try:
            if context.get('skip_prompt_generation'):
                return

            llm_instance = context.get('llm_instance')
            messages = context.get('llm_messages')

            if context.get('verbose'):
                logger.info(f"{self.name}: Sending the following messages to the LLM: {messages}")

            try:
                response = llm_instance.chat(messages)
            except Exception as e:
                if context.get('verbose'):
                    logger.error(f"{self.name}: An error occurred during LLM request: {e}")
                context['llm_response'] = None
                return

            if context.get('verbose'):
                logger.info(f"{self.name}: Received the following response from the LLM: {response}")

            if not response or '```python' not in response:
                if context.get('verbose'):
                    logger.error(f"{self.name}: LLM request returned no valid response")
                context['llm_response'] = None
            else:
                context['llm_response'] = self.extract_code_from_response(response)
                if context.get('verbose'):
                    logger.info(f"{self.name}: LLM request completed")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during LLM request: {e}")
            context['llm_response'] = None
            return

    @staticmethod
    def extract_code_from_response(response):
        """
        Extract the code from the LLM response
        :param response:
        :return:
        """
        try:
            start = response.find('```python') + len('```python')
            end = response.find('```', start)
            return response[start:end].strip()
        except Exception as e:
            logger.error(f"Error extracting code from response: {e}")
            return None
