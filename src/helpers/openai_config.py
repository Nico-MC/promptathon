#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
from src.helpers.console_colors import ConsoleColors

class OpenAIConfig:
    @staticmethod
    def setup():
        print(f"{ConsoleColors.OKCYAN}Configuring OpenAI ...{ConsoleColors.ENDC}")
        openai.api_type = os.getenv("OPENAI_API_TYPE")
        openai.api_base = os.getenv("OPENAI_API_BASE")
        openai.api_version = os.getenv("OPENAI_API_VERSION")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print(f"{ConsoleColors.OKGREEN}Configuring OpenAI finished.{ConsoleColors.ENDC}")