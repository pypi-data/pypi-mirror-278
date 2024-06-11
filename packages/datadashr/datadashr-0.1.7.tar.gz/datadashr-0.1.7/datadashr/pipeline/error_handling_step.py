from datadashr.pipeline.data_step import DataStep
from datadashr.config import *


class ErrorHandlingStep(DataStep):
    def execute(self, context):
        """
            Executes the error handling step in the pipeline.

            Args:
            - context: A dictionary containing information about the current pipeline context.

            Returns:
            - None
            """
        try:
            response = context.get('sandbox_response')
            error = response.get('error') if response else None
            if error:
                llm_instance = context.get('llm_instance')
                full_code = context.get('llm_response') or ''
                error = response.get('error')
                prompt_manager = context.get('prompt_manager')
                messages = prompt_manager.build_prompt_error_messages(full_code, error)

                if context.get('verbose'):
                    logger.info(f"{self.name}: Sending the following error correction messages to the LLM: {messages}")

                error_response = llm_instance.chat(messages)

                if context.get('verbose'):
                    logger.info(
                        f"{self.name}: Received the following error correction response from the LLM: {error_response}")

                context['error_response'] = error_response
                if context.get('verbose'):
                    logger.info(f"{self.name}: Error handling step completed")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during error handling: {e}")
            context['error_response'] = None
            return
