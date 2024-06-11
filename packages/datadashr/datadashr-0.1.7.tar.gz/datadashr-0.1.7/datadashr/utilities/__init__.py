import re
from datadashr.config import *


class Utilities:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def clean_code(self, code) -> str:
        code_blocks = [
            r"```(?:python)?(.*?)```"
        ]
        extracted_code = ""
        for pattern in code_blocks:
            matches = re.finditer(pattern, code, flags=re.DOTALL)
            for match in matches:
                if match:
                    # Aggiunge il codice estratto direttamente a una stringa, mantenendo le formattazioni
                    if extracted_code:  # Se non è la prima aggiunta, inserisce una linea vuota come separatore
                        extracted_code += "\n\n"
                    extracted_code += match.group(1).strip()
        if self.verbose:
            logger.info(f"Extracted code: {extracted_code}")
        return extracted_code