import json

def load_json(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            data = json.load(file)
            print(data)

    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
    except json.JSONDecodeError:
        print(f"Die Datei {file_path} konnte nicht als JSON geparsed werden. Stellen Sie sicher, dass es eine gültige JSON-Datei ist.")
    except UnicodeDecodeError:
        print(f"Die Datei {file_path} konnte nicht mit der Kodierung {encoding} gelesen werden.")
