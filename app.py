from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
import requests
import sqlite3

app = Flask(__name__)
load_dotenv()

api_key = os.getenv("API_KEY")
SEASON = 2024


def get_db_connection():
    conn = sqlite3.connect("players.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            age INTEGER,
            nationality TEXT,
            position TEXT,
            valuation_score REAL
        )
    """)

    conn.commit()
    conn.close()


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


def calculate_valuation_score(age, goals, assists, minutes, position, tackles, interceptions, duels_won, passes_total, key_passes, pass_accuracy):
    if position == "Defender":
        performance_score = defensive_score(
            tackles, interceptions, duels_won, minutes)

    elif position == "Midfielder":
        performance_score = midfield_score(
            assists, key_passes, passes_total, pass_accuracy, duels_won, minutes)

    elif position == "Attacker":
        performance_score = attacking_score(goals, assists, minutes)

    else:
        performance_score = 50

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


def build_player_data(stats_data):
    if stats_data["results"] == 0:
        return None

    all_statistics = stats_data["response"][0]["statistics"]

    best_stat = None
    highest_minutes = 0

    for stat in all_statistics:
        minutes = stat["games"]["minutes"]

        if minutes is not None and minutes > highest_minutes:
            best_stat = stat
            highest_minutes = minutes

    if best_stat is None:
        return None

    player = stats_data["response"][0]["player"]
    statistics = best_stat

    games = statistics["games"]
    goals = statistics["goals"]
    tackles = statistics["tackles"]
    duels = statistics["duels"]
    passes = statistics["passes"]

    goal_total = goals["total"] or 0
    assist_total = goals["assists"] or 0
    minutes_played = games["minutes"] or 0

    tackles_total = tackles["total"] or 0
    interceptions_total = tackles["interceptions"] or 0
    duels_won = duels["won"] or 0

    passes_total = passes["total"] or 0
    key_passes = passes["key"] or 0
    pass_accuracy = passes["accuracy"] or 0

    player_data = {
        "player_id": player["id"],
        "name": player["name"],
        "age": player["age"],
        "nationality": player["nationality"],
        "position": games["position"],
        "appearances": games["appearences"],
        "minutes": minutes_played,
        "goals": goal_total,
        "assists": assist_total,
        "tackles": tackles_total,
        "interceptions": interceptions_total,
        "duels_won": duels_won,
        "passes": passes_total,
        "key_passes": key_passes,
        "pass_accuracy": pass_accuracy,
        "valuation_score": calculate_valuation_score(player["age"], goal_total, assist_total, minutes_played, games["position"], tackles_total, interceptions_total,
                                                     duels_won, passes_total, key_passes, pass_accuracy)
    }

    return player_data


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

    player_data = build_player_data(stats_data)

    if player_data is None:
        return render_template(
            "index.html",
            error="No statistics found"
        )

    return render_template(
        "player.html",
        player=player_data
    )


@app.route("/compare", methods=["GET", "POST"])
def compare_players():

    if request.method == "POST":

        # STAGE 2:
        # User has selected the exact players
        if "player1_id" in request.form and "player2_id" in request.form:

            player1_id = int(request.form["player1_id"])
            player2_id = int(request.form["player2_id"])

            player1_stats = get_player_stats(player1_id)
            player2_stats = get_player_stats(player2_id)

            player1_data = build_player_data(player1_stats)
            player2_data = build_player_data(player2_stats)

            if player1_data is None or player2_data is None:
                return render_template(
                    "compare.html",
                    error="Statistics could not be found for one or both players"
                )

            return render_template(
                "compare.html",
                player1=player1_data,
                player2=player2_data
            )

        # STAGE 1:
        # User searches for two names
        player1_name = request.form["player1"]
        player2_name = request.form["player2"]

        player1_search = search_player(player1_name)
        player2_search = search_player(player2_name)

        if player1_search["results"] == 0 or player2_search["results"] == 0:
            return render_template(
                "compare.html",
                error="One or both players could not be found"
            )

        player1_options = []
        player2_options = []

        for result in player1_search["response"]:
            player = result["player"]

            player1_options.append({
                "id": player["id"],
                "name": player["name"],
                "age": player["age"],
                "nationality": player["nationality"]
            })

        for result in player2_search["response"]:
            player = result["player"]

            player2_options.append({
                "id": player["id"],
                "name": player["name"],
                "age": player["age"],
                "nationality": player["nationality"]
            })

        return render_template(
            "compare.html",
            player1_options=player1_options,
            player2_options=player2_options
        )

    return render_template("compare.html")


@app.route("/watchlist/add", methods=["POST"])
def add_to_watchlist():
    player_id = request.form["player_id"]
    name = request.form["name"]
    age = request.form["age"]
    nationality = request.form["nationality"]
    position = request.form["position"]
    valuation_score = request.form["valuation_score"]

    conn = get_db_connection()

    conn.execute("""
        INSERT OR IGNORE INTO watchlist
        (player_id, name, age, nationality, position, valuation_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        player_id,
        name,
        age,
        nationality,
        position,
        valuation_score
    ))

    conn.commit()
    conn.close()

    return "Player saved to watchlist"


@app.route("/watchlist")
def watchlist():
    conn = get_db_connection()

    players = conn.execute(
        "SELECT * FROM watchlist"
    ).fetchall()

    conn.close()

    return render_template(
        "watchlist.html",
        players=players
    )


@app.route("/watchlist/remove/<int:player_id>", methods=["POST"])
def remove_from_watchlist(player_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM watchlist WHERE player_id = ?",
        (player_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/watchlist")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

# Exercises
