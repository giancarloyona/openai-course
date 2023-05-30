from flask import Flask, render_template, request
from openai import api_key, Completion
from dotenv import dotenv_values
import json

config = dotenv_values('../../.env')
api_key = config['OPENAI_API_KEY']

app = Flask(__name__, template_folder='./templates',
            static_url_path="",
            static_folder="static")


def get_colors(text):
    prompt = f"You are an assistant that generates color palettes based on prompts. \
        You should generate a palette that fits the the theme, mood, or instructions in the prompt. \
        The palette should be between 2 and 8 colors. \
        Desired format: a JSON array with the colors' hexadecimal value. \
        Q: {text} \
        A: "

    response = Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=200
    )

    colors = json.loads(response["choices"][0]["text"])
    return {"colors": colors}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/palette', methods=["POST"])
def prompt_palette():
    app.logger.info("Inside /palette route")
    query = request.form.get("query")
    colors = get_colors(query)
    return colors


if __name__ == "__main__":
    app.run(debug=True)
