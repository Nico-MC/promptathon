from flask import Flask, request, jsonify
from flask_cors import CORS
from src.init import *

app = Flask(__name__)
CORS(app)

@app.route('/getCategoriesForGoaeNumber', methods=['POST'])
def get_categories_for_goae_number():
    data = request.get_json()
    print(data)
    numbers = data['numbers']
    prompt_count = data['promptCount']
    prompts = data['prompts']
    if prompt_count == "1":
        write_comments_after_prefix(numbers)
        json_data = read_json("group_comments_after_prefix.json")
        json_data = get_categories_for_prefix(json_data, numbers)
        write_categories_in_json("categories_for_prefix.json", json_data)
        return jsonify(json_data)
    exit()
    

if __name__ == '__main__':
    app.run(debug=True)