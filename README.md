Football Scouting & Player Valuation Platform

A Flask-based football scouting application that retrieves real-world player data from the API-Football REST API and is being extended from a rule-based valuation system into a supervised machine-learning pipeline for player market-value prediction.

Status: In development. The current application supports player search, player profiles, season-statistics retrieval and an explainable weighted valuation baseline. The next stage is to train, evaluate and deploy a genuine ML regression model.

Why I Built This

I started this project to combine my interest in football with software engineering and data-driven decision-making. The first version used a transparent weighted scoring formula so that I could build the full application flow before introducing machine learning.

The current development goal is to keep that original formula as a baseline and test whether trained regression models can make more accurate player-value predictions from historical performance data.

Current Features

Dynamic football-player search

Multiple search-result selection using unique player IDs

Individual player profile pages

API-Football REST API integration

Retrieval and processing of season statistics

Selection of the most relevant returned statistics using minutes played

Explainable, position-aware rule-based valuation score

Handling of missing or incomplete API responses

Secure API-key storage using environment variables

Git/GitHub version control

Current Tech Stack

Python — backend logic and data processing

Flask — web application framework

HTML/CSS — frontend structure and styling

Requests / REST APIs / JSON — football-data retrieval and processing

python-dotenv — environment-variable management

Git & GitHub — version control

How the Current Application Works

A user searches for a football player.

Flask sends the search request to API-Football.

Matching player profiles are returned and displayed.

The user selects the relevant player using the player's unique ID.

The application retrieves that player's season statistics.

Python processes the returned JSON and selects the statistics entry with the highest number of minutes played.

The current rule-based valuation engine produces a score for the player.

The player's profile and valuation score are displayed in the web application.

Valuation Approach

1. Rule-Based Baseline — Current

The first version of the project uses a deliberately simple, explainable scoring formula rather than machine learning.

It currently considers:

Age

Position

Goals

Assists

Minutes played

Goal contributions per 90 minutes

The model converts age and attacking contribution into scores, applies a position adjustment, and combines them using fixed weights. Because the thresholds and weights are manually chosen, this is a rule-based baseline, not a trained ML model.

Keeping this baseline is useful because it gives the machine-learning models something meaningful to compare against.

2. Supervised Machine Learning — In Progress

The next version will treat player valuation as a supervised regression problem.

Instead of manually choosing the relationship between statistics and value, the model will learn patterns from historical examples containing:

Player performance features

Player characteristics

A known historical market value used as the target

The first feature set will focus on reliable data that can be collected consistently, such as:

Age

Position

Appearances

Minutes played

Goals

Assists

Goals and assists per 90 minutes

Position-specific defensive, passing and attacking features can then be added once the initial pipeline is working reliably.

Planned ML Pipeline

The initial training workflow will be:

Collect historical data — build a dataset containing player statistics and corresponding historical market values.

Clean and validate the data — handle missing values, inconsistent fields and duplicate player-season records.

Engineer features — calculate per-90 metrics and encode categorical features such as position.

Create train/validation/test splits — keep evaluation data separate from model training.

Train a simple baseline model — begin with Linear Regression so the behaviour is easy to understand.

Compare stronger models — test models such as Random Forest and Gradient Boosting.

Evaluate performance — compare models using metrics including MAE and RMSE.

Select and save the best pipeline — persist the trained preprocessing and prediction pipeline.

Integrate inference into Flask — use the trained model to generate player-value predictions inside the web application.

Compare ML predictions with the original rule-based baseline — measure whether the learned model provides a meaningful improvement.

Model Evaluation

The main evaluation metrics will be:

MAE (Mean Absolute Error) — average absolute difference between predicted and actual market values

RMSE (Root Mean Squared Error) — places greater weight on larger prediction errors

R² — used as a supporting measure of how much variation in player value the model explains

A key part of the project will be evaluating the model on data it did not train on rather than judging performance on the training set.

ML Tools Planned

pandas — dataset cleaning and feature preparation

scikit-learn — preprocessing, regression models and evaluation

NumPy — numerical operations

joblib — saving and loading the trained model pipeline

Development Roadmap

Build Flask application structure

Integrate API-Football

Implement player search and profile pages

Retrieve and process season statistics

Build explainable rule-based valuation baseline

Handle missing/incomplete API data

Build historical player-value training dataset

Create reusable preprocessing pipeline

Train Linear Regression baseline

Train Random Forest model

Train Gradient Boosting model

Compare models using MAE/RMSE

Save the best-performing trained pipeline

Integrate ML predictions into Flask

Add position-specific performance features

Add player-to-player comparison

Add interactive performance visualisations

Add player watchlists and persistent storage

Deploy the application

Running the Current Project Locally

Clone the repository:

git clone https://github.com/paulwodi06-ui/football-scouting-platform.git

Navigate into the project:

cd football-scouting-platform

Create and activate a Python virtual environment, then install the current dependencies:

pip install flask requests python-dotenv

Create a .env file in the project root:

API_KEY=your_api_football_key

The .env file is excluded from Git and should never be committed.

Run the Flask application:

python app.py

Then open:

http://127.0.0.1:5000

in your browser.

What This Project Demonstrates

The project is designed to combine multiple areas of software and machine-learning engineering:

Building a web application with Flask

Integrating and validating data from an external REST API

Designing an interpretable non-ML baseline

Building a supervised learning dataset

Feature engineering and preprocessing

Training and comparing regression models

Evaluating models on unseen data

Integrating trained-model inference into an application backend

Using Git/GitHub throughout an iterative development process