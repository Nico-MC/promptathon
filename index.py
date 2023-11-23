from dotenv import load_dotenv
import os
from src.helpers.json_loader import load_json, sort_json
from src.templates.openai_prompter import OpenAIPrompter

# load environment variables (.env)
load_dotenv()

# load json file
json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')
comments = sort_json(load_json(json_file, encoding), json_file)
# print(comments["1"][1])

# connect with open ai api
prompter = OpenAIPrompter()
# result = prompter.create_completion("Joshua ist ein", 40)
# print(result)



