import json
from dotenv import load_dotenv
import os
from src.helpers.json_loader import *
from src.prompting.openai_prompter import OpenAIPrompter
from src.prompting.openai_finetuner import OpenAIFinetuner
from src.helpers.console_colors import ConsoleColors
import ast
import re
import time
from collections import defaultdict

load_dotenv()
json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')

json_data = read_json(json_file, encoding)

prompter = OpenAIPrompter()
finetuner = OpenAIFinetuner()


# load environment variables (.env)
# load_dotenv()

# load json file
# json_file = os.getenv('JSON_FILE')
# encoding = os.getenv('ENCODING')
# json_data = sort_json(read_json(json_file, encoding))
# json_data = read_json(json_file, encoding)

# logit_bias = {}
# logit_bias_data = read_json("logit_bias.json")
# for key, value in logit_bias_data.items():
#     tokenIds = getTokenId(key)
#     logit_bias[tokenIds] = value
    # for tokenId in tokenIds:
    #     logit_bias[tokenId] = value

# connect with open ai api
# prompter = OpenAIPrompter()
# finetuner = OpenAIFinetuner()



##### ----- HELPERS ----- #####
def get_categories_out_of_str(str: str):
    if(str == "[]" or str == None or str == ""):
         return []
    
    str = '["' + str + '"]'
    try:
        result = ast.literal_eval(str)
        # result = json.loads(str)
    except Exception as e:
        print(f"{ConsoleColors.FAIL}{str}{ConsoleColors.FAIL}")
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

def write_comments_after_prefix(goae_ids: list[object]) -> None:
    json_file = "group_comments_after_prefix.json"
    comments_after_prefix = read_json(json_file)
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        if goae_id in comments_after_prefix:
            continue
        comments = json_data[goae_id]['kommentare']
        comments_after_prefix[goae_id] = group_comments_after_prefix(comments)
    write_json(comments_after_prefix, json_file)

def load_examples(json_data: str) -> list[any]:
    examples = []
    goae_ids = ["1", "2", "3"] # load prefered_categories from this goae_ids
    for goae_id in goae_ids:
        for prefix, comments in json_data[goae_id].items():
            comments = comments['kommentare']
            for index, comment in enumerate(comments):
                if "prefered_categories" in comment:
                    title = "\"title\": " + "\"" + comment['title'] + "\",\n"
                    text = "\"text\": " + "\"" + comment['text'] + "\"\n"
                    comment_str = title + text
                    comment_str = re.sub(r'<[^>]+>', '', comment_str)
                    examples.append({"role": "user", "content": comment_str})
                    examples.append({"role": "assistant", "content": str(comment["prefered_categories"])})

    return examples






##### ----- PROMPTING ----- #####
def get_categories_for_comment(json_data: dict, goae_ids: list = None): # get categories for each comment
    pre_prompt = "Bitte gib mir 3 1-Wort Kategorien, die für den folgenden Kommentar passend sind und ärztliche Fachbegriffe sind.\n\n"
    post_prompt = "Die 3 am besten passenden Kategorien sind: [\""
    
    all_comments_in_prefix = ""

    pre_prefix_prompt = "Für die folgenden Kommentare werden nun Stichworte gesucht..."
    post_prefix_prompt = "Falls das Array leer ist, lautet das Ergebnis null. Falls nicht, wird das Wort aus dem Array gefiltert, das inhaltlich mit den obigen aufgezählten Kommentaren am besten übereinstimmt. Am besten sind Worte mit medizinischem Hintergrund. Wörter mit medizinischen Behandlungsmethoden haben immer Vorang. Das Stichwort ist:"
    
    for goae_id in goae_ids:
        if(goae_id == None):
            return
        j = 0
        for prefix, comments in json_data[goae_id].items():
            comments = comments['kommentare']
            all_categories_in_prefix = []
            all_comments_in_prefix_temp = ""
            i = 1
            for index, comment in enumerate(comments):
                prompt = pre_prompt
                title = "\"header\": " + "\"" + comment['title'] + "\", "
                text = "\"body\": " + "\"" + comment['text'] + "\" }"
                comment_str = title + text
                comment_str = re.sub(r'<[^>]+>', '', comment_str)
                obj = "\"Kommentar " + str(i) + "\": { "
                obj += comment_str
                obj += "\n\n"
                all_comments_in_prefix_temp += obj
                prompt += obj
                prompt += post_prompt
                print(f"{ConsoleColors.OKCYAN}----- GOÄ {goae_id} | PREFIX {prefix} | KOMMENTAR {index + 1} | PROMPT {i} -----{ConsoleColors.ENDC}")
                print(prompt)
                categories = prompter.create_completion(prompt,model="gpt-3.5-turbo-instruct", temperature=1, top_p=0.1, max_tokens=100, frequency_penalty=0, presence_penalty=0, stop=["\"]"])
                categories = get_categories_out_of_str(categories)
                for category in categories:
                    all_categories_in_prefix.append(category)
                print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
                json_data[goae_id][prefix]["kommentare"][index]["kategorien"] = categories
                i += 1
            j += 1
            prefix_prompt = pre_prefix_prompt
            prefix_prompt += "\n\n"
            prefix_prompt += all_comments_in_prefix_temp
            prefix_prompt += "Die gefundenen Stichworte wurden in ein Array gepackt und sind: "
            prefix_prompt += str(all_categories_in_prefix) + ". "
            prefix_prompt += post_prefix_prompt
            print(f"{ConsoleColors.OKCYAN}----- GOÄ {goae_id} | PREFIX {prefix} | PROMPT {j} -----{ConsoleColors.ENDC}")
            print(prefix_prompt)
            prefix_categories = prompter.create_completion(prefix_prompt,model="gpt-3.5-turbo-instruct", temperature=1, top_p=0.1, max_tokens=100, frequency_penalty=0, presence_penalty=0, stop=["\n"])
            prefix_categories = re.sub(r'[^\w\s]', '', prefix_categories)
            prefix_categories = prefix_categories.lstrip()
            # prefix_categories = get_categories_out_of_str(prefix_categories)
            print(f"{ConsoleColors.OKGREEN}>{prefix_categories}<{ConsoleColors.ENDC}\n\n")
            json_data[goae_id][prefix]["kategorie"] = prefix_categories
    return json_data

def get_categories_for_prefix(json_data: dict, goae_ids: list = None): # get categories for each prefix
    pre_prompt = "Bitte gib mir 2 1-Wort Kategorien, die für alle der folgenden Kommentare passend sind und ärztliche Fachbegriffe sind.\n\n"
    post_prompt = "Die 2 am besten passenden Kategorien sind: [\""

    for goae_id in goae_ids:
        goae_id = str(goae_id)
        print(goae_id)
        if(goae_id == None):
            return
        j = 0
        for prefix, comments in json_data[goae_id].items():
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
            j += 1
            prompt += post_prompt
            print(f"{ConsoleColors.OKCYAN}----- PROMPT {j} -----{ConsoleColors.ENDC}")
            print(prompt)
            categories = prompter.create_completion(prompt,model="gpt-3.5-turbo-instruct", temperature=1, top_p=0.1, max_tokens=100, frequency_penalty=0, presence_penalty=0, stop=["\"]"])
            categories = get_categories_out_of_str(categories)
            print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
            json_data[goae_id][prefix]["kategorien"] = categories
    return json_data
    
    
def create_categories(json_data: dict, goae_ids: list[str], prompts: list[str]): # function for the frontend prompt button
    # --- iterate over goae numbers --- #
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        print(goae_id)
        if(goae_id == None):
            return
        j = 0
        # --- iterate over prefixes --- #
        for prefix, comments in json_data[goae_id].items():
            comments = comments['kommentare']
            prompt_for_prefix = prompts[0]
            all_comments_in_prefix = ""
            i = 1
            # --- iterate over comments --- #
            for comment in comments:
                title = "\"header\": " + "\"" + comment['title'] + "\", "
                text = "\"body\": " + "\"" + comment['text'] + "\" }"
                comment_str = title + text
                comment_str = re.sub(r'<[^>]+>', '', comment_str)
                all_comments_in_prefix += "\"Kommentar " + str(i) + "\": { "
                all_comments_in_prefix += comment_str
                if i == len(comments):
                    continue
                all_comments_in_prefix += "\n\n"
                i += 1
            j += 1
            prompt_for_prefix = prompt_for_prefix.replace("$comments", all_comments_in_prefix)
            print(f"{ConsoleColors.OKCYAN}----- GOÄ {goae_id} | PREFIX {prefix} | PROMPT {j} -----{ConsoleColors.ENDC}")
            print(prompt_for_prefix)
            categories = prompter.create_completion(prompt=prompt_for_prefix,model="gpt-3.5-turbo-instruct", temperature=1, top_p=0.1, max_tokens=100, frequency_penalty=0, presence_penalty=0, stop=["\"]"])
            categories = get_categories_out_of_str(categories)
            print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
            json_data[goae_id][prefix]["kategorien"] = categories
    return json_data

# goae_ids = ["1", "2"]
# write_comments_after_prefix(goae_ids)
# json_data = read_json("group_comments_after_prefix.json")
# json_data = get_categories_for_prefix(json_data, goae_ids)
# write_categories_in_json("categories_for_prefix.json", json_data)
# json_data = get_categories_for_comment(json_data, goae_ids)
# write_categories_in_json("categories_for_comment.json", json_data)










def create_categories_from_assistant(json_data: dict, goae_ids: list[str], prompts: list[str]):
    examples = load_examples(json_data)
    prompt = [
        {"role": "system", "content": prompts[0]},
        *examples
    ]
    # --- iterate over goae numbers --- #
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        if(goae_id == None):
            return
        j = 0
        # --- iterate over prefixes --- #
        for prefix, comments in json_data[goae_id].items():
            comments = comments['kommentare']
            # prompt_for_prefix = prompts[0]
            # all_comments_in_prefix = ""
            i = 1
            # --- iterate over comments --- #
            for index, comment in enumerate(comments):
                title = "\"title\": " + "\"" + comment['title'] + "\",\n"
                text = "\"text\": " + "\"" + comment['text'] + "\"\n"
                comment_str = title + text
                comment_str = re.sub(r'<[^>]+>', '', comment_str)
                # all_comments_in_prefix += "\"Kommentar " + str(i) + "\": { "
                # all_comments_in_prefix += comment_str
                # if i == len(comments):
                #     continue
                # all_comments_in_prefix += "\n\n"
                i += 1

                # print(prompt)
                temp_prompt = prompt[:]
                temp_prompt.append({"role": "user", "content": comment_str})
                print(f"{ConsoleColors.OKCYAN}----- GOÄ {goae_id} | PREFIX {prefix} | KOMMENTAR {index + 1} -----{ConsoleColors.ENDC}")
                # print(temp_prompt)
                categories = prompter.create_chat(temp_prompt,model="gpt-3.5-turbo-1106", temperature=0.9, top_p=0.1, max_tokens=100, frequency_penalty=0, presence_penalty=0, stop=None)
                # categories = get_categories_out_of_str(categories)
                print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
                json_data[goae_id][prefix]["kommentare"][index]["kategorien"] = categories
            j += 1
            # prompt_for_prefix = prompt_for_prefix.replace("$comments", all_comments_in_prefix)
            # print(f"{ConsoleColors.OKCYAN}----- GOÄ {goae_id} | PREFIX {prefix} | PROMPT {j} -----{ConsoleColors.ENDC}")
            # print(prompt_for_prefix)
            # categories = prompter.create_completion(prompt=prompt_for_prefix,model="gpt-3.5-turbo-instruct", temperature=1, top_p=0.1, max_tokens=100, frequency_penalty=0, presence_penalty=0, stop=["\"]"])
            # categories = get_categories_out_of_str(categories)
            # print(f"{ConsoleColors.OKGREEN}{categories}{ConsoleColors.ENDC}\n\n")
            # json_data[goae_id][prefix]["kategorien"] = categories
    return json_data