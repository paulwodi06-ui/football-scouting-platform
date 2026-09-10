# Football Scouting & Player Valuation Platform

A full-stack football scouting web application built with Python and Flask that allows users to search for players, analyse performance statistics, compare players and save players to a persistent watchlist.

The application integrates with the API-Football REST API and uses an explainable, position-specific scoring model to generate player valuation scores.

## Features

- Search for football players using API-Football
- Select the correct player from multiple search results
- View individual player profiles and season statistics
- Position-specific player valuation model
- Separate scoring logic for:
  - Attackers
  - Midfielders
  - Defenders
- Per-90 performance metrics
- Handles missing or incomplete API data
- Selects the most relevant statistics when multiple competitions are returned
- Compare two players side-by-side
- Resolve ambiguous player searches before comparison
- Visualise player valuation scores using Chart.js
- Save players to a watchlist
- Persistent watchlist storage using SQLite
- Remove players from the watchlist
- Responsive navigation between Search, Compare and Watchlist pages

## Tech Stack

- **Python** — backend logic and valuation model
- **Flask** — web framework
- **HTML/CSS** — frontend structure and styling
- **Jinja2** — dynamic HTML templates
- **REST APIs / JSON** — football data retrieval and processing
- **SQLite** — persistent watchlist storage
- **Chart.js** — player comparison visualisation
- **Git & GitHub** — version control

## Player Valuation Model

The platform uses an explainable scoring system rather than a black-box valuation model.

A player's final score combines:

- Age
- Position-specific performance
- Per-90 statistics

### Attackers

Attackers are evaluated using metrics including:

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

The resulting performance score is combined with an age score to produce a valuation score out of 100.

## How It Works

1. The user searches for a football player.
2. The application sends a request to API-Football.
3. Matching players are displayed.
4. The user selects the correct player.
5. Flask retrieves that player's season statistics.
6. Python processes and cleans the API response.
7. The most relevant competition statistics are selected.
8. A position-specific valuation score is calculated.
9. The player profile is displayed.

Players can also be compared side-by-side or saved to a persistent SQLite watchlist.

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/paulwodi06-ui/football-scouting-platform.git