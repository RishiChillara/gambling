from enum import Enum

class PlayerProp:
    def __init__(self):
        self.athleteName = None
        self.league = None
        self.line = None
        self.propTitle = None
    
    def __init__(self, athleteName, propTitle, line, league):
        self.league = league
        self.athleteName = athleteName
        self.line = line
        self.propTitle = propTitle


class MLBProps(Enum):
     STRIKEOUTS = 1
     HITSALLOWED=2
     EARNEDRUNSALLOWED=3
     WALKSALLOWED=4
     OUTS=5
     SINGLES=6
     TOTALBASES=7
     RBI=8
     HITS=9
     STEALS=10

class WNBAProps(Enum):
    POINTS = 1
    REBOUNDS = 2
    ASSISTS = 3

prop_alias = {
    "Strikeouts": MLBProps.STRIKEOUTS,
    "Pitcher Strikeouts" : MLBProps.STRIKEOUTS,
    "Hits Allowed": MLBProps.HITSALLOWED,
    "Earned Runs Allowed": MLBProps.EARNEDRUNSALLOWED,
    "Walks Allowed": MLBProps.WALKSALLOWED,
    "Pitching Outs": MLBProps.OUTS,
    "Outs": MLBProps.OUTS,
    "Singles": MLBProps.SINGLES,
    "Total Bases": MLBProps.TOTALBASES,
    "RBIs": MLBProps.RBI,
    "Runs Batted In": MLBProps.RBI,
    "Hits": MLBProps.HITS,
    "Steals": MLBProps.STEALS,
    "player-points": WNBAProps.POINTS,
    "player-rebounds": WNBAProps.REBOUNDS,
    "player-assists": WNBAProps.ASSISTS,
    "Points" : WNBAProps.POINTS,
    "Rebounds": WNBAProps.REBOUNDS,
    "Assists": WNBAProps.ASSISTS
    }

def calculate_no_vig_percent(american_odds1, american_odds2):
        
    # Convert american odds to implied probabilities
    implied_prob1 = american_to_implied_prop(american_odds1)
    implied_prob2 = american_to_implied_prop(american_odds2)
    
    # Calculate the market's total probability (including the vig)
    total_market_prob = implied_prob1 + implied_prob2
    
    # Calculate no-vig probabilities
    no_vig_prob1 = implied_prob1 / total_market_prob
    no_vig_prob2 = implied_prob2 / total_market_prob
    
    return no_vig_prob1, no_vig_prob2



def decimal_to_american(decimal):
    if decimal >= 2.00:
        return round((decimal - 1) * 100)
    return round(-100/(decimal - 1))


def american_to_implied_prop(american):
    if american > 0:
        return (100 / (american + 100))
    else:
        return (-1 * american) / ((-1 * american) + 100)