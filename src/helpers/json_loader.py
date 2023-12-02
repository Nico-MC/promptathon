import json
from src.helpers.console_colors import ConsoleColors

def sort_json(json_data: str) -> dict[str, object]:
    json_dict = {str(item["id"]): item for item in json_data}
    write_json(json_dict, 'ziffern_sorted.json')
    return json_dict

def write_categories_in_json(goae_id: str, comment_id: int, categories: list):
    with open('ziffern_sorted.json', 'r') as file:
        json_data = json.load(file)

    try:
        json_data[goae_id]["kommentare"][comment_id]["categories"] = categories
    except IndexError:
        print("null reference in json_data.")

    write_json(json_data, 'ziffern_sorted_with_categories.json')


def write_json(obj: any, file: str, indent: int = 4, ensure_ascii: bool = False):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=indent, ensure_ascii=ensure_ascii)
        print(f"File '{file}' was written successfully.\n")
    except json.JSONDecodeError as e:
        print(f"Error while serializing the object to JSON: {e}")
    except IOError as e:
        print(f"IO error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def read_json(json_file: str, encoding: str='utf-8') -> json:
    json_data = ""
    try:
        print(f"{ConsoleColors.OKCYAN}Loading JSON file {json_file} ...{ConsoleColors.ENDC}")
        with open(json_file, 'r', encoding=encoding) as file:
            json_data = json.load(file)
        print(f"{ConsoleColors.OKGREEN}Loading JSON file {json_file} finished.{ConsoleColors.ENDC}\n")
        return json_data

    except FileNotFoundError:
        print(f"{ConsoleColors.FAIL}The file {json_file} was not found.{ConsoleColors.ENDC}")
    except json.JSONDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be parsed as JSON. Make sure it is a valid JSON file.{ConsoleColors.ENDC}")
    except UnicodeDecodeError:
        print(f"{ConsoleColors.FAIL}The file {json_file} could not be read with the encoding {encoding}.{ConsoleColors.ENDC}")