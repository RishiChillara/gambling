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
    lines: List[float], 
    results: List[float],
    bets: List[BetType],
    bet_type: BetType, 
    bet_amount: float
) -> float:
    """Calculates payoff for a prize picks parlay

    Args:
        lines (List[float]): Betting lines
        results (List[float]): Actual results
        bets (List[BetType]): Over/Under bets on each line
        bet_type (BetType): What kind of bet was the parlay
        bet_amount (float): How much money was placed on the parlay
    Returns:
        payout (float): Total money paid out (includes money put in)
    """
    # Sanity checks 
    assert len(lines) == len(results)
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

if __name__ == "__main__":
    lines = [29.5, 32.0, 1.5, 0.5, 4.5]
    results = [30.0, 31.0, 2.0, 1.0, 4.0]
    bets = [Bet.OVER, Bet.UNDER, Bet.OVER, Bet.OVER, Bet.UNDER]
    bet_type = BetType.FIVE_BET_FLEX
    bet_amount = 400
    payout = payoff_calculator(
        lines, 
        results, 
        bets, 
        bet_type, 
        bet_amount
    )
    print(f"Payout is {payout}")



