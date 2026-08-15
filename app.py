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
        player_name = request.form["player"]

        data = get_player_data(player_name)

        player = data["response"][0]["player"]
        statistics = data["response"][0]["statistics"][0]

        games = statistics["games"]
        goals = statistics["goals"]

        player_data = {
            "name": player["name"],
            "age": player["age"],
            "nationality": player["nationality"],
            "position": games["position"],
            "appearances": games["appearences"],
            "minutes": games["minutes"],
            "goals": goals["total"],
            "assists": goals["assists"]
        }

        return render_template("index.html", player=player_data)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
