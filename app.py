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


def calculate_valuation_score(age, goals, assists, minutes, position, tackles, interceptions, duels_won, passes_total, key_passes, pass_accuracy):
    if position == "Defender":
        performance_score = defensive_score(
            tackles, interceptions, duels_won, minutes)

    elif position == "Midfielder":
        performance_score = midfield_score(
            assists, key_passes, passes_total, pass_accuracy, duels_won, minutes)

    elif position == "Attacker":
        performance_score = attacking_score(goals, assists, minutes)

    score = age_score(age) * 0.4 + performance_score * 0.6

    return round(score, 1)


def defensive_score(tackles, interceptions, duels_won, minutes):
    if minutes == 0:
        return 0

    tackles_per_90 = tackles / minutes * 90
    interceptions_per_90 = interceptions / minutes * 90
    duels_won_per_90 = duels_won / minutes * 90

    tackle_score = min(tackles_per_90 / 2.5 * 100, 100)
    interception_score = min(interceptions_per_90 / 2.0 * 100, 100)
    duel_score = min(duels_won_per_90 / 6.0 * 100, 100)

    score = (
        tackle_score * 0.3
        + interception_score * 0.3
        + duel_score * 0.4
    )

    return round(score, 1)


def attacking_score(goals, assists, minutes):
    if minutes == 0:
        return 0

    goals_per_90 = goals / minutes * 90
    assists_per_90 = assists / minutes * 90
    contributions_per_90 = (goals + assists) / minutes * 90

    goal_score = min(goals_per_90 / 0.8 * 100, 100)
    assist_score = min(assists_per_90 / 0.5 * 100, 100)
    contribution_score_value = min(contributions_per_90 / 1.0 * 100, 100)

    score = (
        goal_score * 0.5
        + assist_score * 0.2
        + contribution_score_value * 0.3
    )

    return round(score, 1)


def midfield_score(assists, key_passes, passes_total, pass_accuracy, duels_won, minutes):
    if minutes == 0:
        return 0

    assists_per_90 = assists / minutes * 90
    key_passes_per_90 = key_passes / minutes * 90
    passes_per_90 = passes_total / minutes * 90
    duels_won_per_90 = duels_won / minutes * 90

    assist_score = min(assists_per_90 / 0.5 * 100, 100)
    key_pass_score = min(key_passes_per_90 / 2.5 * 100, 100)
    passing_volume_score = min(passes_per_90 / 70 * 100, 100)
    accuracy_score = min(pass_accuracy / 90 * 100, 100)
    duel_score = min(duels_won_per_90 / 6 * 100, 100)

    score = (
        assist_score * 0.20
        + key_pass_score * 0.25
        + passing_volume_score * 0.20
        + accuracy_score * 0.20
        + duel_score * 0.15
    )

    return round(score, 1)


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
    tackles = statistics["tackles"]
    duels = statistics["duels"]
    passes = statistics["passes"]

    tackles_total = tackles["total"] or 0
    interceptions_total = tackles["interceptions"] or 0
    duels_won = duels["won"] or 0
    minutes_played = games["minutes"] or 0

    defensive_score(
        tackles_total,
        interceptions_total,
        duels_won,
        minutes_played)

    passes_total = passes["total"] or 0
    key_passes = passes["key"] or 0
    pass_accuracy = passes["accuracy"] or 0

    goal_total = goals["total"] or 0
    assist_total = goals["assists"] or 0

    player_data = {
        "name": player["name"],
        "age": player["age"],
        "nationality": player["nationality"],
        "position": games["position"],
        "appearances": games["appearences"],
        "minutes": minutes_played,
        "goals": goal_total,
        "assists": assist_total,
        "valuation_score": calculate_valuation_score(player["age"], goal_total, assist_total, minutes_played, games["position"], tackles_total,
                                                     interceptions_total, duels_won, passes_total, key_passes, pass_accuracy)
    }

    return render_template(
        "player.html",
        player=player_data
    )


if __name__ == "__main__":
    app.run(debug=True)


# Exercises
