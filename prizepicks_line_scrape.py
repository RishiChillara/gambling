from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from helper import PlayerProp
from helper import prop_alias
from IPython.display import display

import json 
import pandas as pd

#TODO: Pass in driver instead of creating a new one
def scapePrizePicksLines(driver):
    """
    Scrapes all Prizepicks Lines
    
    Returns:
    pandas dataframe: [Name, Prop Title, Line, League]
    """

    url = "view-source:https://api.prizepicks.com/projections"

    driver.get(url)

    content = driver.page_source
    content = driver.find_element(By.TAG_NAME, 'pre').text


    prop_data = json.loads(content)
    id_to_name = {}
    props = []

    for i in range(len(prop_data["included"])):
        player_id = prop_data["included"][i]["id"]

        # Catch malformed data
        try: 
            athlete_name = prop_data["included"][i]["attributes"]["name"]
            league = prop_data["included"][i]["attributes"]["league"]
        except KeyError:
            continue

        id_to_name[player_id] = [athlete_name, league]

    for i in range(len(prop_data["data"])):
        player_id = prop_data["data"][i]["relationships"]["new_player"]["data"]["id"]
        prop_title = prop_data["data"][i]["attributes"]["stat_type"]
        
        if prop_title in prop_alias:
             prop_title =  str(prop_alias[prop_title])
        line = float(prop_data["data"][i]["attributes"]["line_score"])
 
        props.append(PlayerProp(id_to_name[player_id][0], prop_title, line, id_to_name[player_id][1]))

   

    return pd.DataFrame([(prop.athleteName, prop.line, prop.propTitle, prop.league) for prop in props], columns=["Name", "Line", "Prop Title", "League"])



