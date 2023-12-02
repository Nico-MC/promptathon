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
        
    def get_categories(self,
                    prompt: str,
                    max_tokens: int = None,
                    temperature: float = None,
                    top_p: float = None,
                    n: int = None,
                    stream: bool = None,
                    seed: int = None,
                    stop: list[str] = None, # ["Ende", "Schluss", "Fazit"]
                    presence_penalty: float = 0,
                    frequency_penalty: float = 0,
                    response_format: str = None, # Must be one of `text` or `json_object`
                    logit_bias: dict[str, int] = {}, # mein_dict = { "schlüssel1": 10, "schlüssel2": 20, "schlüssel3": 30 }
                    user: str = "",
                    timeout: float = None,
                    model="TestDeployment"
                    ) -> str:
        try:
            if self._client is None:
                print(f"{ConsoleColors.FAIL}_client is none. Please check AzureOpenAI initialization.{ConsoleColors.ENDC}\n")
                return None
            
            # print(f"{ConsoleColors.OKCYAN}Send following prompt:\n{prompt}{ConsoleColors.ENDC}")
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    # system: Dies definiert eine Systemnachricht, die Anweisungen oder Informationen für das Modell enthält, wie es antworten soll.
                    {"role": "system", "content": """
                     Lese Titel und Text und gebe ausschließlich 3 passende Stichworte aus. Es ist wichtig, dass die Stichworte individuell sind
                     und sich nicht ähneln. Man soll den Text anhand der Stichworte wiederfinden können.
                     Ignoriere Quellenverweise, falls diese vorkommen.
                    """},
                    # user: Nachricht des Benutzers
                    {"role": "user", "content": prompt},
                    # assistant: Dies sind Antworten, die das Modell in früheren Dialogen generiert hat. Sie geben Kontext und zeigen,
                    # wie das Modell auf vorherige Benutzeranfragen reagiert hat.
                    {"role": "assistant", "content": """
                     Kategorie1,Kategorie2,Kategorie3
                    """},
                    # {"role": "user", "content": "Where was it played?"}
                ],
                temperature=temperature, # Beeinflusst die Kreativität der Antworten. Ein höherer Wert führt zu kreativeren, aber möglicherweise weniger präzisen Antworten
                max_tokens=max_tokens, # Legt die maximale Anzahl von Tokens (Wörtern und Zeichen) fest, die in der Antwort generiert werden.
                top_p=top_p, # Steuert die Diversität der Antwort durch Begrenzung der Token-Auswahl auf einen bestimmten Prozentsatz der wahrscheinlichsten Tokens.
                              #je näher an 1 desto mehr Kreativität, je näher an 0 desto konsistenter
                n=n, # Anzahl der Komplettierungen
                stream=stream, # Wenn True, werden die Antworten als kontinuierlicher Stream zurückgegeben, anstatt auf die vollständige Antwort zu warten.
                seed=seed, # If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters
                            # should return the same result. Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.
                stop=stop, # Hier können Sie Zeichenketten (Strings) definieren, bei denen die Komplettierung stoppen soll.
                            # Dies ist nützlich, um Antworten auf eine bestimmte Länge zu begrenzen oder um zu verhindern,
                            # dass das Modell über einen bestimmten Punkt hinaus generiert."""
                presence_penalty=presence_penalty, # erhöht die Wahrscheinlichkeit, dass neue und unterschiedliche Themen in den Antworten erscheinen.
                response_format=response_format, # Bestimmt das Format der Antwort, zum Beispiel ob sie als Text, JSON, etc. zurückgegeben wird.
                frequency_penalty=frequency_penalty, # reduziert die Wahrscheinlichkeit, bereits erwähnte Themen oder Begriffe zu wiederholen, was zu vielfältigeren Antworten führen kann.
                logit_bias=logit_bias, # Erlaubt die Anpassung der Wahrscheinlichkeiten bestimmter Tokens beim Generieren von Antworten.
                                        # Kann verwendet werden, um bestimmte Wörter oder Phrasen zu fördern oder zu vermeiden.
                user=user, # Ein optionaler Parameter, der es ermöglicht, die Komplettierungen auf der Grundlage einer spezifischen Benutzer-ID zu personalisieren.
                timeout=timeout # Ein Zeitlimit für die API-Anfrage.
            )
            result = response.choices[0].message.content
            result = [item.strip().rstrip('.') for item in result.split(',')]
            print(f"{ConsoleColors.OKGREEN}Kategorien: {result}{ConsoleColors.ENDC}\n")
            return result
        except Exception as e:
            print(f"An error occurred on sending create_chat: {e}")
            return None