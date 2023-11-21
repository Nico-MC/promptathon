#Note: The openai-python library support for Azure OpenAI is in preview.
import os
from openai import AzureOpenAI
from src.helpers.console_colors import ConsoleColors

class OpenAIConfig:
    @staticmethod
    def setup():
        try:
            print(f"{ConsoleColors.OKCYAN}Configuring OpenAI ...{ConsoleColors.ENDC}")
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),  
                api_version=os.getenv("AZURE_OPENAI_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            )
            print(f"{ConsoleColors.OKGREEN}Configuring OpenAI finished.{ConsoleColors.ENDC}\n")
        except Exception as e:
            print(f"There was a problem connecting to OpenAI API. Please consider checking .env.\nError message: {e}")