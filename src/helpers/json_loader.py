import json
import tiktoken
from src.helpers.console_colors import ConsoleColors

def sort_json(json_data: str) -> dict[str, object]:
    json_dict = {str(item["id"]): item for item in json_data}
    write_json(json_dict, 'ziffern_sorted.json')
    return json_dict

def write_categories_in_json(json_file: str, categories: list[str]) -> None:
    write_json(categories, json_file)

def write_training_property_in_json(json_file: str, data: str) -> None:
    write_json(data, json_file)
    
def write_training_data_in_json(json_file: str, training_data: list) -> None:
    with open(json_file, "w", encoding='utf-8') as file:
        for obj in training_data:
            json_string = json.dumps(obj, ensure_ascii=False)
            file.write(json_string + '\n')

def write_json(obj: any, file: str, indent: int = 4, ensure_ascii: bool = False) -> None:
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=indent, ensure_ascii=ensure_ascii)
        print(f"{ConsoleColors.OKGREEN}File '{file}' was written successfully.{ConsoleColors.ENDC}\n")
    except json.JSONDecodeError as e:
        print(f"{ConsoleColors.FAIL}Error while serializing the object to JSON: {e}{ConsoleColors.ENDC}")
    except IOError as e:
        print(f"{ConsoleColors.FAIL}IO error occurred: {e}{ConsoleColors.ENDC}")
    except Exception as e:
        print(f"{ConsoleColors.FAIL}An unexpected error occurred: {e}{ConsoleColors.ENDC}")

def read_json(json_file: str, encoding: str='utf-8') -> json:
    json_data = {}
    try:
        print(f"{ConsoleColors.OKCYAN}Loading JSON file {json_file} ...{ConsoleColors.ENDC}")
        with open(json_file, 'r', encoding=encoding) as file:
            json_data = json.load(file)
        print(f"{ConsoleColors.OKGREEN}Loading JSON file {json_file} finished.{ConsoleColors.ENDC}\n")
        return json_data

    except FileNotFoundError:
        print(f"{ConsoleColors.FAIL}The file {json_file} was not found.{ConsoleColors.ENDC}")
        return json_data
    except json.JSONDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be parsed as JSON. Make sure it is a valid JSON file.{ConsoleColors.ENDC}")
    except UnicodeDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be read with the encoding {encoding}.{ConsoleColors.ENDC}")


def getTokenId(word: str, model="gpt-3.5-turbo-0301") -> list:
    enc = tiktoken.encoding_for_model(model)
    return enc.encode(word)[0]