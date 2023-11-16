from dotenv import load_dotenv
import os
from src.helpers.json_loader import load_json
from src.helpers.openai_config import OpenAIConfig
from src.helpers.console_colors import ConsoleColors

# load environment variables (.env)
load_dotenv()

# load json file
json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')
load_json(json_file, encoding)

# connect with open ai api
OpenAIConfig.setup()