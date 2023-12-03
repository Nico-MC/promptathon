from dotenv import load_dotenv
import os
from src.helpers.json_loader import read_json, sort_json, write_categories_in_json
from src.templates.openai_prompter import OpenAIPrompter
from src.helpers.console_colors import ConsoleColors

# load environment variables (.env)
load_dotenv()

# load json file
json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')
# json_data = sort_json(read_json(json_file, encoding))
json_data = read_json(json_file, encoding)


# connect with open ai api
prompter = OpenAIPrompter()


def write_categories(goae_ids: list[int]) -> None:
    json_file = "categories.json"
    categories_of_goae = read_json(json_file);
    for goae_id in goae_ids:
        goae_id = str(goae_id)
        comments = json_data[goae_id]['kommentare']
        for index, comment in enumerate(comments):
            id = str(comment['id'])
            prefix = comment['prefix']
            title = comment['title']
            text = comment['text']
            comment = "Titel: " + title + "\n" + "Text: " + text
            categories = prompter.get_categories(comment, top_p=0.1)
            if goae_id not in categories_of_goae:
                categories_of_goae[goae_id] = {}
            categories_of_goae[goae_id][id] = categories
            # categories_of_goae[goae_id][id] = {
            #     "prefix": prefix,
            #     "categories": categories,
            # }
    write_categories_in_json(json_file, categories_of_goae);

write_categories([5]);