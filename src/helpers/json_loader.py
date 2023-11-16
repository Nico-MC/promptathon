import json
from src.helpers.console_colors import ConsoleColors

def load_json(json_file, encoding):
    try:
        print(f"{ConsoleColors.OKCYAN}Loading JSON file {json_file} ...{ConsoleColors.ENDC}")
        with open(json_file, 'r', encoding=encoding) as file:
            data = json.load(file)
            # print(data)
        print(f"{ConsoleColors.OKGREEN}Loading JSON file {json_file} finished.\n{ConsoleColors.ENDC}")

    except FileNotFoundError:
        print(f"{ConsoleColors.FAIL}The file {json_file} was not found.{ConsoleColors.ENDC}")
    except json.JSONDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be parsed as JSON. Make sure it is a valid JSON file.{ConsoleColors.ENDC}")
    except UnicodeDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be read with the encoding {encoding}.{ConsoleColors.ENDC}")