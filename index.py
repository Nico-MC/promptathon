import json
from dotenv import load_dotenv
import os
from src.helpers.json_loader import *
from src.templates.openai_prompter import OpenAIPrompter
from src.templates.openai_finetuner import OpenAIFinetuner
from src.helpers.console_colors import ConsoleColors
import ast
import re
import time
from collections import defaultdict


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
    logit_bias[tokenIds] = value
    # for tokenId in tokenIds:
    #     logit_bias[tokenId] = value

# connect with open ai api
prompter = OpenAIPrompter()
finetuner = OpenAIFinetuner()

def get_categories_out_of_str(str: str):
    if(str == "[]" or str == None or str == ""):
         return []
    
    # str = '["' + str + '"]'
    try:
        result = ast.literal_eval(str)
        # result = json.loads(str)
    except Exception as e:
        print(f"An error occurred on sending get_categories_out_of_str: {e}")
        return []
    # result = [item.strip().rstrip('.') for item in result.split(',')]
    return result

def group_comments_after_prefix(comments):
    grouped_comments_by_letter = defaultdict(list)
    for comment in comments:
        match = re.match(r"([a-zA-Z]+)", comment["prefix"])
        letter = match.group(1) if match else ""
        grouped_comments_by_letter[letter].append(comment)

    grouped_comments_by_letter_dict = dict(grouped_comments_by_letter)
    return grouped_comments_by_letter_dict






def write_categories(goae_ids: list[int]) -> None:
    json_file = "categories.json"
    categories_of_goae = read_json(json_file)
    comments_after_prefix = {}
    training_data = []
    # prompt = "Ein Kommentar besteht immer aus einem Titel und zugehörigem Text:\n"
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        comments = json_data[goae_id]['kommentare']
        generations = 0
        abandoned_generations = 0
        max_generations = len(comments)
        prompt = "Bitte gib mir 2 Gruppen, die für alle der folgenden Kommentare passend sind und ausschließlich ärztliche Fachbegriffe sind.\n\n\n"
        for index, comment in enumerate(comments):
            # if(index < 10): 
            # if(index == 10 or index == 12 or index == 26):
                id = str(comment['id'])
                prefix:str = comment['prefix']
                title = "header: " + comment['title'] + ", "
                text = "body: " + comment['text'] + " }"
                training = comment.get('training')
                unchecked_training = comment.get('unchecked_training')
                # comment_str = title + text
                comment_str = title + text
                comment_str = re.sub(r'<[^>]+>', '', comment_str)
                # comment_str = title + "\n" + text
                # categories = prompter.create_chat(comment_str, top_p=0.1)
                # prompt = "Bitte filtere aus folgendem Kommentar medizinische Kategorien. Wenn du keine medizinische Kategorien finden kannst, gebe eine leere Liste aus. Die Kategorien MÜSSEN mit Medizin zu tun haben!\nKommentar: { "
                # prompt = "Bitte filtere aus folgendem Kommentar maximal 5 medizinische Kategorien, die medizinische Behandlungsmethoden gruppieren. Wenn du keine Kategorien in dem Kommentar finden kannst, gebe ein leeres Array aus. Die Kategorien MÜSSEN einen medizinischen Hintergrund haben und die Kategorien müssen klar zeigen, um welche medizinischen oder ärztlichen Maßnahmen es in dem Kommentar geht. Vermeide unbedingt nicht medizinische Kategorien, da sich diese nicht einordnen lassen.\n"

                if(prefix.startswith("b")):
                    prompt += "Kommentar: { "
                    prompt += comment_str + "\n\n"
                else:
                    continue
                # prompt += " -> [\""
                # prompt += """\n\nBitte identifiziere und liste die Schlüsselkategorien dieses Textes auf, basierend auf seinem Inhalt.\nDie Schlüsselkategorien lauten: [\""""
                # if(training != None):
                #     training_data.append(finetuner.create_training_data(prompt, training))


                ### !!! thread kann durch einsetzen der thread_id in url später erneut angeschaut werden !!! ###
                ### !!! https://platform.openai.com/playground?assistant=<assist_id>&thread=<thread_id> !!! ###
                # assistant_id = "asst_VJHdWVFKsjw9WcoARomuK2MI"
                # thread_id = "thread_BXqFK65Mawt1vO4Kr3sOX7Wv"
                # message = prompter.create_assistant_thread_message(thread_id, prompt)
                # run = prompter.run_assistant_thread(assistant_id, thread_id)

                # start_time = time.time()

                # while time.time() - start_time < 10:
                #     status = prompter.retrieve_assistant_thread_status(thread_id,run.id)
                #     if status == "completed":
                #         categories = prompter.retrieve_assistant_thread_message(thread_id, message.id)
                #         break
                #     time.sleep(0.5)




                # categories = prompter.create_completion(prompt,logit_bias=logit_bias, best_of=1, temperature=1, top_p=0.2, max_tokens=100, frequency_penalty=1, presence_penalty=1, stop=["\"]"], user="123456", seed=4)
                # categories = get_categories_out_of_str(categories)
                # json_data[goae_id]['kommentare'][index]['training'] = categories
                # if(training == None or unchecked_training != None):
                #     categories = prompter.create_completion(prompt,temperature=1, top_p=0.2, max_tokens=256, frequency_penalty=1, presence_penalty=1, stop=["\"]"], user="1234", seed=2)
                #     categories = get_categories_out_of_str(categories)
                #     json_data[goae_id]['kommentare'][index]['unchecked_training'] = categories
                # else:
                #     categories = prompter.create_completion(prompt,temperature=1, top_p=0.2, max_tokens=256, frequency_penalty=1, presence_penalty=1, stop=["\"]"], user="1234", seed=2)
                # prompt += categories
                # prompt += "\n\nNehme die wichtigsten 3 medizinische: [\""
                # categories = prompter.create_completion(prompt, temperature=1, top_p=0.2, max_tokens=256, frequency_penalty=0, presence_penalty=0, stop=["\"]"], user="1234", seed=2)
                # print(f"{ConsoleColors.OKCYAN}----- PROMPT {index+1}/{max_generations} -----{ConsoleColors.ENDC}")
                # print(f"{ConsoleColors.OKBLUE}{prompt}{ConsoleColors.ENDC}")
                # print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
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
        prompt += "Die 2 Gruppen sind: [\""
        categories = prompter.create_completion(prompt,temperature=1, top_p=0.2, max_tokens=256, frequency_penalty=0, presence_penalty=0, stop=["\"]"])
        print(categories)
        color = ConsoleColors.OKGREEN if abandoned_generations == 0 else ConsoleColors.WARNING
        print(f"{color}{(generations - abandoned_generations)} / {generations} generated successfully.{ConsoleColors.ENDC}")
        comments_after_prefix[goae_id] = group_comments_after_prefix(comments)
    # write_categories_in_json(json_file, categories_of_goae)
    # write_training_data_in_json("finetuning.jsonl", training_data)
    # write_training_property_in_json('ziffern_sorted.json',json_data)
    write_json(comments_after_prefix, "group_comments_after_prefix.json")

write_categories([1])

# result = prompter.status_finetune()
#
# print(result)