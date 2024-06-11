from datadashr.pipeline.data_step import DataStep
from datadashr.config import *


class PromptGenerationStep(DataStep):
    def execute(self, context):
        """
        Execute the prompt generation step
        :param context:
        :return:
        """
        try:
            if context.get('skip_prompt_generation'):
                return

            prompt_manager = context['prompt_manager']
            request = context['request']
            examples = context['vector_manager'].get_by_vector(request) if context.get('enable_vector') else []
            prompt_content = prompt_manager.build_prompt_for_df(request)
            if examples:
                prompt_content += f"\n\nYou can utilize these examples as a reference for generating code.\n{examples}"

            if context.get('verbose'):
                logger.info(f"Generated prompt content: {prompt_content}")

            messages = [
                {"role": "system", "content": prompt_manager.build_prompt_for_role()},
                {"role": "user", "content": prompt_content}
            ]

            if context.get('verbose'):
                logger.info(f"Messages to be sent to LLM: {messages}")

            context['llm_messages'] = messages
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during prompt generation: {e}")
            context['llm_messages'] = None
            return
