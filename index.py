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

print("----- Beispielausgabe für einen Kommentar -----")
goae_number = "1" #please only give string; can contain letters too.
comment_number = 0
# example how to call a specific comment (see end str)
print(f"GOÄ-Ziffer: {goae_number}\nKommentar-Nr: {comment_number+1}/{len(comments[goae_number])} \
      \n\nKommentar: {comments[goae_number][comment_number]}\n\n")


# connect with open ai api
prompter = OpenAIPrompter()
# result = prompter.create_completion("Joshua ist ein", 40)
# print(result)



