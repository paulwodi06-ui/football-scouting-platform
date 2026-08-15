from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()

api_key = os.getenv("API_KEY")


def get_player_data(player_name):
    url = "https://v3.football.api-sports.io/players"

    headers = {
        "x-apisports-key": api_key
    }

    params = {
        "team": 42,
        "search": player_name
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        player = request.form["player"]

        data = get_player_data(player)

        return render_template("index.html", data=data)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
