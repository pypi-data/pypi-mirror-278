from datadashr.pipeline.data_step import DataStep
from datadashr.sandbox import Sandbox
from datadashr.config import *


class SandboxExecutionStep(DataStep):
    def execute(self, context):
        """
        Execute the sandbox execution step
        :param context:
        :return:
        """
        try:
            llm_response = context.get('llm_response')
            if not llm_response:
                if context.get('verbose'):
                    logger.error(f"{self.name}: LLM response is None")
                context['sandbox_response'] = {'error': 'LLM response is None', 'result': None, 'full_code': None}
                return

            code = llm_response
            if not code:
                if context.get('verbose'):
                    logger.error(f"{self.name}: No code returned by LLM")
                context['sandbox_response'] = {'error': 'No code returned by LLM', 'result': None, 'full_code': None}
                return

            sandbox_instance = Sandbox(context.get('verbose', False))
            sandbox_instance.allow_import("pandas")
            sandbox_instance.allow_import("numpy")
            full_code = f"import pandas as pd\nimport numpy as np\n{code}"
            if context.get('verbose'):
                logger.info(f"{self.name}: full code first pass: {full_code}")

            if context.get('verbose'):
                logger.info(f"{self.name}: Executing the following code in the sandbox: {full_code}")

            response = sandbox_instance.execute(full_code, {"df": context['df']})
            context['sandbox_response'] = {
                "error": response.get('error'),
                "result": response.get('result'),
                "full_code": full_code,
            }
            if context.get('verbose'):
                logger.info(f"{self.name}: Sandbox response: {response}")
                logger.info(f"{self.name}: Sandbox execution completed")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during sandbox execution: {e}")
            context['sandbox_response'] = {'error': str(e), 'result': None, 'full_code': None}
            return
