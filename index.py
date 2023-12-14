import json
from dotenv import load_dotenv
import os
from src.helpers.json_loader import read_json, sort_json, write_categories_in_json
from src.templates.openai_prompter import OpenAIPrompter
from src.helpers.console_colors import ConsoleColors
import ast
import re

# load environment variables (.env)
load_dotenv()

# load json file
json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')
# json_data = sort_json(read_json(json_file, encoding))
json_data = read_json(json_file, encoding)


# connect with open ai api
prompter = OpenAIPrompter()

def get_categories_out_of_str(str: str):
    result = '["' + str + '"]'
    # result = json.loads(result)
    result = ast.literal_eval(result)
    # result = [item.strip().rstrip('.') for item in result.split(',')]
    return result

def write_categories(goae_ids: list[int]) -> None:
    json_file = "categories.json"
    categories_of_goae = read_json(json_file)
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        comments = json_data[goae_id]['kommentare']
        generations = 0
        abandoned_generations = 0
        max_generations = len(comments)
        for index, comment in enumerate(comments):
            # if(index == 6): 
            # if(index == 10 or index == 12 or index == 26):
                id = str(comment['id'])
                prefix = comment['prefix']
                title = comment['title']
                text = comment['text']
                comment = "Titel: " + title + "\n" + "Text: " + text
                comment = re.sub(r'<[^>]+>', '', comment)
                # comment = title + "\n" + text
                # categories = prompter.create_chat(comment, top_p=0.1)
                prompt = "Ein Kommentar besteht immer aus einem Titel und zugehörigem Text:\n\n"
                prompt += comment
                prompt += "\n\nBitte identifiziere aus diesem Text nur die spezifischen medizinischen Begriffe, die direkt in der Medizin Anwendung finden. Schließe allgemeine oder nicht fachspezifische Begriffe wie 'vorbereitende Maßnahmen' und 'Gebühren' aus: [\""
                prompt += prompter.create_completion(prompt, temperature=1, top_p=0.2, max_tokens=60, frequency_penalty=0, presence_penalty=0, stop=["\"]"], user="1234", seed=2)
                prompt += "\n\nWenn man daraus nur die Begriffe nimmt, die in der Medizin Anwendung finden, erhält man: [\""
                categories = prompter.create_completion(prompt, temperature=1, top_p=0.2, max_tokens=60, frequency_penalty=0, presence_penalty=0, stop=["\"]"], user="1234", seed=2)
                print(f"{ConsoleColors.OKCYAN}----- PROMPT {index+1}/{max_generations} -----{ConsoleColors.ENDC}")
                print(f"{ConsoleColors.OKBLUE}{prompt}{ConsoleColors.ENDC}")
                categories = get_categories_out_of_str(categories)
                print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
                categories = None
                generations += 1
                if(categories == None):
                    abandoned_generations += 1
                if goae_id not in categories_of_goae:
                    categories_of_goae[goae_id] = {}
                # categories_of_goae[goae_id][id] = categories
                categories_of_goae[goae_id][id] = {
                    "index": index,
                    # "prefix": prefix,
                    "title": title,
                    "text": text,
                    "categories": categories,
                }
        color = ConsoleColors.OKGREEN if abandoned_generations == 0 else ConsoleColors.WARNING
        print(f"{color}{(generations - abandoned_generations)} / {generations} generated successfully.{ConsoleColors.ENDC}")
    write_categories_in_json(json_file, categories_of_goae)

write_categories([5])