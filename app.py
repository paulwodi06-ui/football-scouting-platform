from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()

api_key = os.getenv("API_KEY")
SEASON = 2024


def search_player(player_name):
    url = "https://v3.football.api-sports.io/players/profiles"

    headers = {
        "x-apisports-key": api_key
    }

    params = {
        "search": player_name
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()


def get_player_stats(player_id):
    url = "https://v3.football.api-sports.io/players"

    headers = {
        "x-apisports-key": api_key
    }

    params = {
        "id": player_id,
        "season": SEASON
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        player_name = request.form["player"]

        search_data = search_player(player_name)

        if search_data["results"] == 0:
            return render_template("index.html", error="Player not found")

        players = []
        for result in search_data["response"]:
            player = result["player"]

            players.append({
                "id": player["id"],
                "name": player["name"],
                "firstname": player["firstname"],
                "lastname": player["lastname"],
                "age": player["age"],
                "nationality": player["nationality"]
            })

        return render_template("searchresults.html", players=players)

    return render_template("index.html")


@app.route("/player/<int:player_id>")
def player_profile(player_id):
    stats_data = get_player_stats(player_id)

    if stats_data["results"] == 0:
        return render_template(
            "index.html",
            error="No statistics found"
        )

    player = stats_data["response"][0]["player"]
    statistics = stats_data["response"][0]["statistics"][0]

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

    return render_template(
        "player.html",
        player=player_data
    )


if __name__ == "__main__":
    app.run(debug=True)


# Exercises
