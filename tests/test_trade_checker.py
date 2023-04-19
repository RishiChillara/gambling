from gambling.trade_checker import payoff_calculator, payoff_for_multiple_parlays, Bet, BetType


def test_payoff_calculator_five_bet_flex_five_wins():
    lines = [29.5, 32.0, 1.5, 0.5, 4.5]
    results = [30.0, 31.0, 2.0, 1.0, 4.0]
    bets = [Bet.OVER, Bet.UNDER, Bet.OVER, Bet.OVER, Bet.UNDER]
    bet_type = BetType.FIVE_BET_FLEX
    bet_amount = 400
    payout = payoff_calculator(lines, results, bets, bet_type, bet_amount)
    assert payout == 4000

def test_payoff_calculator_five_bet_flex_four_wins():
    lines = [29.5, 32.0, 1.5, 0.5, 4.5]
    results = [30.0, 31.0, 2.0, 1.0, 4.0]
    bets = [Bet.OVER, Bet.UNDER, Bet.OVER, Bet.UNDER, Bet.UNDER]
    bet_type = BetType.FIVE_BET_FLEX
    bet_amount = 400
    payout = payoff_calculator(lines, results, bets, bet_type, bet_amount)
    assert payout == 800

def test_payoff_calculator_five_bet_flex_three_wins():
    lines = [29.5, 32.0, 1.5, 0.5, 4.5]
    results = [30.0, 31.0, 2.0, 1.0, 4.0]
    bets = [Bet.UNDER, Bet.UNDER, Bet.OVER, Bet.UNDER, Bet.UNDER]
    bet_type = BetType.FIVE_BET_FLEX
    bet_amount = 400
    payout = payoff_calculator(lines, results, bets, bet_type, bet_amount)
    assert payout == 160

def test_payoff_for_multiple_parlays():
    parlay_1_lines = [390.5, 1.5, 65.5]
    parlay_2_lines = [0.5, 1.5, 2.5, 3.5]
    parlay_3_lines = [4.5, 67.5, 10.0, 14.5, 15.5]
    parlay_4_lines = [3.5, 7.5, 100.5, 215.5, 38.5, 42.5]

    parlay_1_results = [395.0, 1.0, 67.0]
    parlay_2_results = [1.0, 0.0, 5.0, 3.0]
    parlay_3_results = [4.0, 70.0, 7.0, 30.0, 12.0]
    parlay_4_results = [1.0, 8.0, 94.0, 107.0, 40.0, 50.0]

    parlay_1_bets = [Bet.UNDER, Bet.UNDER, Bet.OVER]
    parlay_2_bets = [Bet.OVER, Bet.UNDER, Bet.UNDER, Bet.OVER]
    parlay_3_bets = [Bet.UNDER, Bet.OVER, Bet.UNDER, Bet.UNDER, Bet.OVER]
    parlay_4_bets = [Bet.UNDER, Bet.OVER, Bet.UNDER, Bet.UNDER, Bet.OVER, Bet.OVER]

    all_bet_types = [BetType.THREE_BET_FLEX, BetType.FOUR_BET_POWER, BetType.FIVE_BET_FLEX, BetType.SIX_BET_FLEX]
    all_bet_amounts = [300, 200, 100, 400]

    all_lines = [parlay_1_lines, parlay_2_lines, parlay_3_lines, parlay_4_lines]
    all_results = [parlay_1_results, parlay_2_results, parlay_3_results, parlay_4_results]
    all_bets = [parlay_1_bets, parlay_2_bets, parlay_3_bets, parlay_4_bets]

    calculated_payout = payoff_for_multiple_parlays(all_lines, all_results, all_bets, all_bet_types, all_bet_amounts)
    expected_payout = 300 * 1.25 + 200 * 0 + 100 * 0.4 + 400 * 25.0

    assert calculated_payout == expected_payout
    