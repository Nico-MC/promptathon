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



##### ----- HELPERS ----- #####
def get_categories_out_of_str(str: str):
    if(str == "[]" or str == None or str == ""):
         return []
    
    str = '["' + str + '"]'
    try:
        result = ast.literal_eval(str)
        # result = json.loads(str)
    except Exception as e:
        print(str)
        print(f"An error occurred on sending get_categories_out_of_str: {e}")
        return []
    # result = [item.strip().rstrip('.') for item in result.split(',')]
    return result

def group_comments_after_prefix(comments):
    grouped_comments_by_letter = defaultdict(lambda: {"kommentare": [], "kategorien": ""})
    for comment in comments:
        match = re.match(r"([a-zA-Z]+)", comment["prefix"])
        letter = match.group(1) if match else ""
        grouped_comments_by_letter[letter]["kommentare"].append(comment)

    grouped_comments_by_letter_dict = dict(grouped_comments_by_letter)
    return grouped_comments_by_letter_dict

def wirte_comments_after_prefix(goae_ids: list[int]) -> None:
    comments_after_prefix = {}
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        comments = json_data[goae_id]['kommentare']
        comments_after_prefix[goae_id] = group_comments_after_prefix(comments)
    write_json(comments_after_prefix, "group_comments_after_prefix.json")






##### ----- PROMPTING ----- #####
pre_prompt = "Bitte gib mir 2 1-Wort Kategorien, die für alle der folgenden Kommentare passend sind und ärztliche Fachbegriffe sind.\n\n"
post_prompt = "Die 2 am besten passenden Kategorien sind: [\""
    
def get_categories_for_prefix(json_data: dict, goae_ids: list = None):
    for goae_id in goae_ids:
        if(goae_id == None):
            return
        data = json_data[goae_id]
        y = 0
        for prefix, comments in data.items():
            prompt = pre_prompt
            comments = comments['kommentare']
            i = 1
            for comment in comments:
                title = "\"header\": " + "\"" + comment['title'] + "\", "
                text = "\"body\": " + "\"" + comment['text'] + "\" }"
                comment_str = title + text
                comment_str = re.sub(r'<[^>]+>', '', comment_str)
                prompt += "\"Kommentar " + str(i) + "\": { "
                prompt += comment_str
                prompt += "\n\n"
                i += 1
            y += 1
            prompt += post_prompt
            print(f"{ConsoleColors.OKCYAN}----- PROMPT {y} -----{ConsoleColors.ENDC}")
            print(prompt)
            categories = prompter.create_completion(prompt,model="gpt-3.5-turbo",logit_bias=logit_bias, best_of=1, temperature=1, top_p=0.1, max_tokens=100, frequency_penalty=0, presence_penalty=0, stop=["\"]"])
            categories = get_categories_out_of_str(categories)
            print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
            json_data[goae_id][prefix]["kategorien"] = categories
    return json_data

goae_ids = ["1"]
wirte_comments_after_prefix(goae_ids)
json_data = read_json("group_comments_after_prefix.json")
json_data = get_categories_for_prefix(json_data, goae_ids)
write_categories_in_json("group_comments_after_prefix.json", json_data)