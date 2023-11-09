from dotenv import load_dotenv
import os
from json_loader import load_json

load_dotenv()

json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')
load_json(json_file, encoding)
