# Football Scouting & Player Valuation Platform

A Flask-based web application for searching, analysing and evaluating football players using real-world performance data from the API-Football REST API.

> **Status:** In development — currently expanding the player valuation model with position-specific performance metrics and additional scouting features.

## Overview

The platform allows users to search for football players, select from matching results and view player profiles containing season performance statistics.

It also includes an explainable player valuation model written in Python. The model currently considers factors including age, position, minutes played and goal contributions per 90, with further position-specific metrics being added.

## Current Features

* Dynamic football player search
* Multiple search-result selection using unique player IDs
* Individual player profile pages
* Integration with the API-Football REST API
* Retrieval of player information and season statistics
* Position-aware player valuation scoring
* Handling of missing/incomplete API data
* Selection of relevant statistics when multiple competitions are returned
* Secure API-key storage using environment variables
* Git/GitHub version control

## Tech Stack

* **Python** — backend logic and player valuation model
* **Flask** — web application framework
* **HTML/CSS** — frontend structure and styling
* **REST API / JSON** — retrieval and processing of football data
* **Git & GitHub** — version control

## How It Works

1. A user searches for a football player.
2. Flask sends the search request to API-Football.
3. Matching player profiles are returned and displayed.
4. The user selects the relevant player.
5. The application retrieves that player's season statistics using their unique player ID.
6. Python processes the returned JSON data and selects the most relevant statistics.
7. The application calculates a player valuation score and displays the player's profile.

## Valuation Model

The current valuation model uses factors including:

* Age
* Position
* Goals
* Assists
* Minutes played
* Goal contributions per 90 minutes

The model is being expanded to use position-specific statistics so that defenders, midfielders and attackers are assessed using metrics more relevant to their roles.

## Planned Features

* Position-specific defensive, passing and attacking metrics
* Player-to-player comparison
* Interactive performance visualisations
* Player watchlists
* Persistent storage using SQLite
* Improved valuation methodology
* Improved responsive UI
* Deployment of the web application

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/paulwodi06-ui/football-scouting-platform.git
```

Navigate into the project:

```bash
cd football-scouting-platform
```

Create and activate a Python virtual environment, then install the required dependencies.

Create a `.env` file in the project root:

```text
API_KEY=your_api_football_key
```

The `.env` file is excluded from Git and should never be committed.

Run the Flask application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

in your browser.
