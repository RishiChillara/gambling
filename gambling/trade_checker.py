from enum import Enum
from typing import List

import numpy as np


class Bet(Enum):
    UNDER = 0
    OVER = 1


class BetType(Enum):
    TWO_BET_POWER = 1
    THREE_BET_FLEX = 2
    THREE_BET_POWER = 3
    FOUR_BET_FLEX = 4
    FOUR_BET_POWER = 5
    FIVE_BET_FLEX = 6
    SIX_BET_FLEX = 7


PAYOFFS = {
    BetType.TWO_BET_POWER: [0.0, 0.0, 3.0],
    BetType.THREE_BET_FLEX: [0.0, 0.0, 1.25, 2.25],
    BetType.THREE_BET_POWER: [0.0, 0.0, 0.0, 5.0],
    BetType.FOUR_BET_FLEX: [0.0, 0.0, 0.0, 1.5, 5.0],
    BetType.FOUR_BET_POWER: [0.0, 0.0, 0.0, 0.0, 10.0],
    BetType.FIVE_BET_FLEX: [0.0, 0.0, 0.0, 0.4, 2.0, 10.0],
    BetType.SIX_BET_FLEX: [0.0, 0.0, 0.0, 0.0, 0.4, 2.0, 25.0],
}


def payoff_calculator(
    lines: List[float], results: List[float], bets: List[Bet], bet_type: BetType, bet_amount: float
) -> float:
    """Calculates payoff for a prize picks parlay

    Args:
        lines (List[float]): Betting lines
        results (List[float]): Actual results
        bets (List[Bet]): Over/Under bets on each line
        bet_type (BetType): What kind of bet was the parlay
        bet_amount (float): How much money was placed on the parlay
    Returns:
        payout (float): Total money paid out (includes money put in)
    """
    # Sanity checks
    assert len(lines) == len(results) == len(bets)
    num_legs_parlay = len(lines)
    payoff_scheme = PAYOFFS[bet_type]
    assert len(payoff_scheme) - 1 == len(lines)

    lines = np.array(lines)
    results = np.array(results)

    bet_outcomes = (results > lines).astype(np.int32)

    bets_placed = np.array([bet.value for bet in bets])
    num_bets_won = sum(bets_placed == bet_outcomes)

    payout = bet_amount * payoff_scheme[num_bets_won]

    return payout


def payoff_for_multiple_parlays(
    all_lines: List[List[float]],
    all_results: List[List[float]],
    all_bets: List[List[Bet]],
    all_bet_types: List[BetType],
    all_bet_amounts: List[float],
) -> float:
    """Calculate payouts for multiple parlays. Useful utility method
       for calculating results for an entire week.

    Args:
        all_lines (List[List[float]]): Betting lines for each parlay
        all_results (List[List[float]]): Results for each parlay
        all_bets (List[List[Bet]]): The bet on each line on each parlay
        all_bet_types (List[BetType]): The type of parlay for each parlay
        all_bet_amounts (List[float]): How much money was placed on each parlay

    Returns:
        payout (float): Total payout
    """
    assert (
        len(all_lines)
        == len(all_results)
        == len(all_bets)
        == len(all_bet_types)
        == len(all_bet_amounts)
    )
    total_payout = 0

    for (lines, results, bets, bet_type, bet_amount) in zip(
        all_lines, all_results, all_bets, all_bet_types, all_bet_amounts
    ):
        total_payout += payoff_calculator(lines, results, bets, bet_type, bet_amount)

    return total_payout

