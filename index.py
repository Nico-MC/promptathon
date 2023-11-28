from dotenv import load_dotenv
import os
from src.helpers.json_loader import load_json, sort_json
from src.templates.openai_prompter import OpenAIPrompter
from src.helpers.console_colors import ConsoleColors

# load environment variables (.env)
load_dotenv()

# load json file
json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')
comments = sort_json(load_json(json_file, encoding))


# connect with open ai api
prompter = OpenAIPrompter()

comment = comments[3032]['kommentare'][0]
title = comment['title']
text = comment['text']
comment = "Titel: " + title + "\n" + "Text: " + text

result = prompter.create_chat(comment, 200, 1)
print(f"{ConsoleColors.OKGREEN}{result}{ConsoleColors.ENDC}\n")


