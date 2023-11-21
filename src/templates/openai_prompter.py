import os
from openai import AzureOpenAI
from src.helpers.console_colors import ConsoleColors

class OpenAIPrompter:
    def __init__(self):
        try:
            print(f"{ConsoleColors.OKCYAN}Configuring OpenAI ...{ConsoleColors.ENDC}")
            self._client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),  
                api_version=os.getenv("AZURE_OPENAI_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            )
            print(f"{ConsoleColors.OKGREEN}Configuring OpenAI finished.{ConsoleColors.ENDC}\n")
        except Exception as e:
            print(f"There was a problem connecting to OpenAI API. Please consider checking .env.\nError message: {e}")

    def create_completion(self, prompt: str, max_tokens: int, model="TestDeployment") -> str:
        try:
            if self._client is None:
                print(f"{ConsoleColors.FAIL}_client is none. Please check AzureOpenAI initialisation.{ConsoleColors.ENDC}\n")
                return None
            
            response = self._client.completions.create(model=model, prompt=prompt, max_tokens=max_tokens)
            return response.choices[0].text
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None