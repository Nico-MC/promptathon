import json

file_path = 'mgi_confidential.json'

try:
    # Versuch, die Datei mit der ISO-8859-1 Kodierung zu öffnen
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        data = json.load(file)
        print(data)

except FileNotFoundError:
    print(f"Die Datei {file_path} wurde nicht gefunden.")
except json.JSONDecodeError:
    print(f"Die Datei {file_path} konnte nicht als JSON geparsed werden. Stellen Sie sicher, dass es eine gültige JSON-Datei ist.")
except UnicodeDecodeError:
    print(f"Die Datei {file_path} konnte nicht mit der Kodierung 'iso-8859-1' gelesen werden.")
