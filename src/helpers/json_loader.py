import json
from src.helpers.console_colors import ConsoleColors
from collections import defaultdict

def load_json(json_file: str, encoding: str):
    comments = ""
    try:
        print(f"{ConsoleColors.OKCYAN}Loading JSON file {json_file} ...{ConsoleColors.ENDC}")
        with open(json_file, 'r', encoding=encoding) as file:
            comments = json.load(file)
        print(f"{ConsoleColors.OKGREEN}Loading JSON file {json_file} finished.{ConsoleColors.ENDC}\n")
        return comments

    except FileNotFoundError:
        print(f"{ConsoleColors.FAIL}The file {json_file} was not found.{ConsoleColors.ENDC}")
    except json.JSONDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be parsed as JSON. Make sure it is a valid JSON file.{ConsoleColors.ENDC}")
    except UnicodeDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be read with the encoding {encoding}.{ConsoleColors.ENDC}")


def sort_json(json: str):
    json_dict = {item["id"]: item for item in json}
    return json_dict