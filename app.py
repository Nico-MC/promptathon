from flask import Flask, render_template, request
import index

app = Flask(__name__, template_folder='src/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-prompts', methods=['POST'])
def submit_prompts():
    prompt_count = int(request.form.get('promptCount', 0))
    prompts = [request.form.get(f'prompt{i}') for i in range(prompt_count)]
    return "Prompts erhalten: " + str(prompts)

if __name__ == '__main__':
    app.run(debug=True)