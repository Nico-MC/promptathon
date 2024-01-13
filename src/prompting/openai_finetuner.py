import json
import os
import re

from src.helpers.console_colors import ConsoleColors
from src.helpers.json_loader import write_json

class OpenAIFinetuner:
    def __init__(self):
        try:
            print(f"{ConsoleColors.OKCYAN}Creating Finetuner ...{ConsoleColors.ENDC}")
            
            print(f"{ConsoleColors.OKGREEN}Creating Finetuner finished.{ConsoleColors.ENDC}\n")
        except Exception as e:
            print(f"There was a problem finetuning the OpenAI model. Please consider checking finetuner.py.\nError message: {e}")

    def create_training_data(self, prompt: str, training: list) -> dict:
        # Histologie", "Präparat", "Gebühren", "Analognummern
        completion = '", "'.join(training) + '"].'
        training_data = {
            "prompt": prompt,
            "completion": completion
        }
        return training_data
