from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()

api_key = os.getenv("API_KEY")
SEASON = 2024


def age_score(age):
    if age < 22:
        return 100
    elif age < 25:
        return 90
    elif age < 28:
        return 80
    elif age < 31:
        return 65
    else:
        return 45


def contribution_score(goals, assists, minutes):
    goal_contributions = goals + assists
    if minutes == 0:
        return 0
    contributions_per_90 = goal_contributions / minutes * 90
    if contributions_per_90 >= 0.8:
        return 100
    elif contributions_per_90 >= 0.6:
        return 85
    elif contributions_per_90 >= 0.4:
        return 70
    elif contributions_per_90 >= 0.2:
        return 50
    else:
        return 30


def calculate_valuation_score(age, goals, assists, minutes, position):
    score = age_score(age) * 0.4 + position_adjusted_score(position, contribution_score(goals,
                                                                                        assists, minutes)) * 0.6
    return round(score, 1)


def position_adjusted_score(position, contribution_score):
    if position == "Attacker":
        return contribution_score
    elif position == "Midfielder":
        return min(contribution_score * 1.1, 100)
    elif position == "Defender":
        return min(contribution_score * 1.25, 100)
    else:
        return 50


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

    all_statistics = stats_data["response"][0]["statistics"]
    best_stat = None
    highest_minutes = 0

    for stat in all_statistics:
        minutes = stat["games"]["minutes"]

        if minutes is not None and minutes > highest_minutes:
            best_stat = stat
            highest_minutes = minutes

    player = stats_data["response"][0]["player"]
    statistics = best_stat

    games = statistics["games"]
    goals = statistics["goals"]

    goal_total = goals["total"] or 0
    assist_total = goals["assists"] or 0
    minutes_played = games["minutes"] or 0

    player_data = {
        "name": player["name"],
        "age": player["age"],
        "nationality": player["nationality"],
        "position": games["position"],
        "appearances": games["appearences"],
        "minutes": minutes_played,
        "goals": goal_total,
        "assists": assist_total,
        "valuation_score": calculate_valuation_score(
            player["age"],
            goal_total,
            assist_total,
            minutes_played,
            games["position"]
        )
    }

    return render_template(
        "player.html",
        player=player_data
    )


if __name__ == "__main__":
    app.run(debug=True)


# Exercises
