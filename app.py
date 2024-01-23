from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from src.init import *

app = Flask(__name__)
CORS(app)

def custom_jsonify(data, status_code=200):
    return Response(json.dumps(data, ensure_ascii=False), 
                    status=status_code, 
                    content_type='application/json; charset=utf-8')

@app.route('/getCategoriesForGoaeNumber', methods=['POST'])
def get_categories_for_goae_number():
    try:
        data = request.get_json()
        print(data)
        numbers = data['numbers']
        prompt_count = data['promptCount']
        prompts = data['prompts']


        write_comments_after_prefix(numbers)
        json_data = read_json("group_comments_after_prefix.json")
        json_data = create_categories(json_data, numbers, prompts)
        # write_categories_in_json("categories_for_prefix.json", json_data)
        return jsonify(json_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        data = custom_jsonify({"error": "Bei 'get_categories_for_prefix' in der init.py gab es wohl einen Fehler.\nMöglicherweise gibt der prompt keine vernünftige Antwort zurück.", "message": str(e)}, 500)
        return data

# this method use the assistant (see tab 'chat' on openai playground)
@app.route('/getCategoriesForGoaeNumberFromAssistant', methods=['POST'])
def get_categories_for_goae_number_from_assistant():

        data = request.get_json()
        numbers = data['numbers']
        prefixes = data['prefixes']
        prompt_count = data['promptCount2']
        prompts = data['prompts2']

        write_comments_after_prefix(numbers)
        json_data = read_json("group_comments_after_prefix.json")
        json_data = create_categories_from_assistant(json_data, numbers, prefixes, prompts, format=True)



        # format json result
        # formatted_json_data = json_data
        # for outer_key, outer_value in json_data.items():
        #     for inner_key, inner_value in outer_value.items():
        #         if 'kommentare' in inner_value:
        #             neue_kommentare = []
        #             for kommentar in inner_value['kommentare']:
        #                 reduzierter_kommentar = {
        #                     'ziffernNr': kommentar.get('zifferNr', ''),
        #                     'title': kommentar.get('title', ''),
        #                     'text': kommentar.get('text', ''),
        #                     # 'categories': inner_value.get('kategorien', '')  # Annahme: 'kategorien' ist auf der gleichen Ebene wie 'kommentare'
        #                 }
        #                 neue_kommentare.append(reduzierter_kommentar)
        #             # Ersetzen Sie die alte 'kommentare'-Liste durch die neue Liste
        #             inner_value['kommentare'] = neue_kommentare
        # print(json_data)




        write_categories_in_json("categories_for_prefix.json", json_data)
        return jsonify({"1": "lel"})


if __name__ == '__main__':
    app.run(debug=True)