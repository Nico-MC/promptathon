# We use this file to experiment with completions

from openai import OpenAI
from src.helpers.console_colors import ConsoleColors

class OpenAIPrompter:
    def __init__(self):
        print(f"{ConsoleColors.OKCYAN}Init openai_prompter...{ConsoleColors.ENDC}")

    def send_prompt(self, prompt, model, max_tokens):
        try:
            client = OpenAI()
            response = client.completions.create(model=model, prompt=prompt, max_tokens=max_tokens)
            return response.choices[0].text
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None