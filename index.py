import json
from dotenv import load_dotenv
import os
from src.helpers.json_loader import *
from src.templates.openai_prompter import OpenAIPrompter
from src.templates.openai_finetuner import OpenAIFinetuner
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

logit_bias = {}
logit_bias_data = read_json("logit_bias.json")
for key, value in logit_bias_data.items():
    tokenIds = getTokenId(key)
    for tokenId in tokenIds:
        logit_bias[tokenId] = value

# connect with open ai api
prompter = OpenAIPrompter()
finetuner = OpenAIFinetuner()

def get_categories_out_of_str(str: str):
    if(str == None or str == ""):
         return []
    result = '["' + str + '"]'
    # result = json.loads(result)
    result = ast.literal_eval(result)
    # result = [item.strip().rstrip('.') for item in result.split(',')]
    return result

def write_categories(goae_ids: list[int]) -> None:
    json_file = "categories.json"
    categories_of_goae = read_json(json_file)
    training_data = []
    # prompt = "Ein Kommentar besteht immer aus einem Titel und zugehörigem Text:\n"
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        comments = json_data[goae_id]['kommentare']
        generations = 0
        abandoned_generations = 0
        max_generations = len(comments)
        for index, comment in enumerate(comments):
            # if(index == 0): 
            # if(index == 10 or index == 12 or index == 26):
                id = str(comment['id'])
                prefix = comment['prefix']
                title = comment['title']
                text = comment['text']
                training = comment.get('training')
                unchecked_training = comment.get('unchecked_training')
                comment = "Titel: " + title + "\n" + "Text: " + text
                comment = re.sub(r'<[^>]+>', '', comment)
                # comment = title + "\n" + text
                # categories = prompter.create_chat(comment, top_p=0.1)
                prompt = "Der folgende Kommentar besteht aus einem Titel und einem Text. Bitte extrahiere aus diesem Kommentar maximal 5 medizinische Begriffe. Falls die Begriffe nicht medizinisch sind, gebe die Liste einfach leer aus.\nKommentar: '"
                prompt += comment
                prompt += "'. -> [\""
                # prompt += """\n\nBitte identifiziere und liste die Schlüsselkategorien dieses Textes auf, basierend auf seinem Inhalt.\nDie Schlüsselkategorien lauten: [\""""
                # if(training != None):
                #     training_data.append(finetuner.create_training_data(prompt, training))
                categories = ""
                categories = prompter.create_completion(prompt, best_of=10, temperature=0.5, top_p=0.2, max_tokens=256, frequency_penalty=1, presence_penalty=1, stop=["\"]"], user="12345", seed=3)
                categories = get_categories_out_of_str(categories)
                # if(training == None or unchecked_training != None):
                #     categories = prompter.create_completion(prompt,temperature=1, top_p=0.2, max_tokens=256, frequency_penalty=1, presence_penalty=1, stop=["\"]"], user="1234", seed=2)
                #     categories = get_categories_out_of_str(categories)
                #     json_data[goae_id]['kommentare'][index]['unchecked_training'] = categories
                # else:
                #     categories = prompter.create_completion(prompt,temperature=1, top_p=0.2, max_tokens=256, frequency_penalty=1, presence_penalty=1, stop=["\"]"], user="1234", seed=2)
                # prompt += categories
                # prompt += "\n\nNehme die wichtigsten 3 medizinische: [\""
                # categories = prompter.create_completion(prompt, temperature=1, top_p=0.2, max_tokens=256, frequency_penalty=0, presence_penalty=0, stop=["\"]"], user="1234", seed=2)
                print(f"{ConsoleColors.OKCYAN}----- PROMPT {index+1}/{max_generations} -----{ConsoleColors.ENDC}")
                print(f"{ConsoleColors.OKBLUE}{prompt}{ConsoleColors.ENDC}")
                print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
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
    # write_training_data_in_json("finetuning.jsonl", training_data)
    # write_training_property_in_json('ziffern_sorted.json',json_data)

write_categories([1])

# result = prompter.status_finetune()
#
# print(result)