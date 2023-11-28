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

    def create_completion(self, prompt: str, max_tokens: int, temperature: float, model="TestDeployment") -> str:
        try:
            if self._client is None:
                print(f"{ConsoleColors.FAIL}_client is none. Please check AzureOpenAI initialization.{ConsoleColors.ENDC}\n")
                return None
            
            response = self._client.completions.create(model=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
            return response.choices[0].text
        except Exception as e:
            print(f"An error occurred on sending create_completion: {e}")
            return None
        
    def create_chat(self, prompt: str, max_tokens: int, temperature: float, model="TestDeployment") -> str:
        try:
            if self._client is None:
                print(f"{ConsoleColors.FAIL}_client is none. Please check AzureOpenAI initialization.{ConsoleColors.ENDC}\n")
                return None
            
            print(f"{ConsoleColors.OKCYAN}Send following prompt:\n{prompt}{ConsoleColors.ENDC}")
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    # system: Dies definiert eine Systemnachricht, die Anweisungen oder Informationen für das Modell enthält, wie es antworten soll.
                    {"role": "system", "content": "Du bist ein Assistent für einen Sachbearbeiter und solltst den gegebenen Text in Stichworte kategorisieren."},
                    # user: Nachricht des Benutzers
                    {"role": "user", "content": prompt},
                    # assistant Dies sind Antworten, die das Modell in früheren Dialogen generiert hat. Sie geben Kontext und zeigen,
                    # wie das Modell auf vorherige Benutzeranfragen reagiert hat.
                    {"role": "assistant", "content": """
                     Hier eine Beispielauflistung, von einem vorherigen Ergebnis:
                     1. Abrechnung
                     2. Stationäre Behandlung
                     3. Leistungsnummern"""},
                    # {"role": "user", "content": "Where was it played?"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred on sending create_chat: {e}")
            return None