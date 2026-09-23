
from app import (
    age_score,
    attacking_score,
    defensive_score,
    midfield_score,
    calculate_valuation_score
)


def test_age_score_boundaries():
    assert age_score(21) == 100
    assert age_score(22) == 90
    assert age_score(25) == 80
    assert age_score(28) == 65
    assert age_score(31) == 45


def test_defensive_score_zero_minutes():
    assert defensive_score(5, 3, 10, 0) == 0


def test_defensive_score_maximum():
    assert defensive_score(5, 4, 12, 180) == 100


def test_defensive_score_weighting():
    assert defensive_score(0, 2, 0, 90) == 30


def test_attacking_score_zero_minutes():
    assert attacking_score(10, 5, 0) == 0


def test_attacking_score_maximum():
    assert attacking_score(8, 5, 900) == 100


def test_midfield_score_zero_minutes():
    assert midfield_score(2, 10, 500, 85, 30, 0) == 0


def test_midfield_score_maximum():
    assert midfield_score(5, 25, 700, 90, 60, 900) == 100


def test_final_score_weighting():
    score = calculate_valuation_score(
        age=31,
        goals=8,
        assists=5,
        minutes=900,
        position="Attacker",
        tackles=0,
        interceptions=0,
        duels_won=0,
        passes_total=0,
        key_passes=0,
        pass_accuracy=0
    )

    assert score == 78


def test_unknown_position():
    score = calculate_valuation_score(
        age=22,
        goals=0,
        assists=0,
        minutes=900,
        position="Goalkeeper",
        tackles=0,
        interceptions=0,
        duels_won=0,
        passes_total=0,
        key_passes=0,
        pass_accuracy=0
    )

    assert score == 66
