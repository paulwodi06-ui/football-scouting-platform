# Football Scouting & Player Valuation Platform

A full-stack football scouting web application built with **Python and Flask** that allows users to search for football players, analyse performance statistics, compare players, generate position-specific valuation scores, and save players to a persistent watchlist.

The application integrates with the **API-Football REST API** and processes real-world player data into structured, comparable metrics.

## Features

- Search for football players using API-Football
- Select the correct player from multiple search results
- View individual player profiles and season statistics
- Compare two players side-by-side
- Visualise player valuation scores using Chart.js
- Save and remove players from a persistent SQLite watchlist
- Handle missing statistic values and unavailable player data
- Select the most relevant statistics when multiple competitions are returned
- Generate position-specific valuation scores for attackers, midfielders, and defenders

## Tech Stack

- **Python** — backend logic and data processing
- **Flask** — web application framework
- **REST APIs / JSON** — football data retrieval and processing
- **SQLite** — persistent watchlist storage
- **HTML/CSS** — frontend structure and styling
- **Jinja2** — dynamic page rendering
- **Chart.js** — player comparison visualisation
- **Requests** — HTTP requests to API-Football
- **python-dotenv** — environment-variable management
- **Git & GitHub** — version control

## How It Works

1. A user searches for a football player.
2. Flask sends a request to the API-Football REST API.
3. Matching players are returned and displayed.
4. The user selects the relevant player.
5. The application retrieves that player's season statistics.
6. Python processes the API response and selects the most relevant statistics.
7. Position-specific performance metrics are calculated.
8. A valuation score is generated.
9. The player profile is displayed.

Players can also be compared side-by-side or saved to a persistent watchlist.

## Player Valuation Model

The application uses an explainable, rule-based scoring model rather than a black-box machine-learning model.

A player's final score combines:

- Age
- Playing time
- Position-specific performance
- Per-90 statistics

### Attackers

Attackers are evaluated using:

- Goals per 90
- Assists per 90
- Goal contributions per 90

### Midfielders

Midfielders are evaluated using:

- Assists per 90
- Key passes per 90
- Passes per 90
- Pass accuracy
- Duels won per 90

### Defenders

Defenders are evaluated using:

- Tackles per 90
- Interceptions per 90
- Duels won per 90

Each set of metrics is converted into a performance score, which is combined with an age score to produce a final valuation score out of 100.

## Handling Real-World API Data

A key part of the project was dealing with API responses that were not always consistent.

The backend:

- Handles missing numerical statistics
- Accounts for players appearing across multiple competitions or teams
- Selects the statistics entry with the highest number of minutes played
- Handles cases where no usable player statistics are returned
- Resolves ambiguous player searches before comparisons

This required building backend logic around the API rather than assuming every response followed the same structure.

## Watchlist

Players can be saved to a persistent watchlist using SQLite.

The database stores:

- Player ID
- Name
- Age
- Nationality
- Position
- Valuation score

Players can also be removed from the watchlist through the application.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/paulwodi06-ui/football-scouting-platform.git
cd football-scouting-platform