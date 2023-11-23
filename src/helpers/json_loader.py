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


def sort_json(comments: str, json_file: str):
    sql_key = list(comments.keys())[0]
    data = comments[sql_key]

    grouped_data = defaultdict(list)
    for entry in data:
        grouped_data[entry["ziffer_nr"]].append(entry)

    output_file_path = 'sorted_'+json_file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(grouped_data, file, ensure_ascii=False, indent=4)

    print(f"{ConsoleColors.OKGREEN}Json file '{output_file_path}' was saved in root directory.{ConsoleColors.ENDC}\n")