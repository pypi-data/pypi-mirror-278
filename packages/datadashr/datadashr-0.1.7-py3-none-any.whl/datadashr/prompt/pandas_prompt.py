from datadashr.config import *
from jinja2 import Environment, FileSystemLoader
from loguru import logger


class PromptManager:
    """
    Class to generate prompts for the user to solve a problem
    """
    def __init__(self, data, custom_prompt: str = "", prompt_override: bool = False, **kwargs):
        """
        Constructor for PromptManager
        :param data:
        :param custom_prompt:
        :param prompt_override:
        """
        self.data = data
        self.custom_prompt = custom_prompt
        self.prompt_override = prompt_override
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.verbose = kwargs.get('verbose', False)

    def _extract_string_columns(self) -> list:
        """
        Extract string columns from the data
        :return:
        """
        try:
            return [col for col in self.data.columns if self.data.dtypes[col] == 'object']
        except Exception as e:
            if self.verbose:
                logger.error(f"Error extracting string columns: {e}")
            return []

    def _all_columns(self) -> list:
        """
        Get all columns in the data
        :return:
        """
        try:
            return self.data.columns.tolist()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error getting all columns: {e}")
            return []

    def build_prompt_for_role(self):
        """
        Build prompt for role
        :return:
        """
        try:
            template = self.env.get_template('role_template.txt')
            return template.render(
                num_rows=len(self.data),
                num_columns=len(self.data.columns),
                columns=self.data.dtypes.items()
            ).strip()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for role: {e}")
            return ""

    def build_prompt_for_df(self, request):
        """
        Build prompt for DataFrame
        :param request:
        :return:
        """
        try:
            if self.prompt_override:
                return self.custom_prompt

            template = self.env.get_template('df_template.txt')
            return template.render(
                num_rows=len(self.data),
                num_columns=len(self.data.columns),
                columns=self.data.dtypes.items(),
                request=request,
                custom_prompt=self.custom_prompt
            ).strip()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for DataFrame: {e}")
            return ""

    def build_prompt_for_error_correction(self, error_message, generated_code):
        """
        Build prompt for error correction
        :param error_message:
        :param generated_code:
        :return:
        """
        try:
            template = self.env.get_template('error_correction_template.txt')
            return template.render(
                error_message=error_message,
                generated_code=generated_code
            ).strip()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for error correction: {e}")
            return ""
