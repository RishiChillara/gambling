from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from helper import PlayerProp
from helper import prop_alias
from IPython.display import display


import json 
import pandas as pd

#returns a dataframe with name, line, prop, and league
def scapeUnderDogLines(driver):

    url = "view-source:https://api.underdogfantasy.com/beta/v4/over_under_lines"
    driver.get(url)

    content = driver.page_source
    content = driver.find_element(By.TAG_NAME, 'pre').text
    prop_data = json.loads(content)

    props = []
    appearance_to_player_id = {}
    id_to_name = {}

    appearances = prop_data["appearances"]
    over_under_lines = prop_data["over_under_lines"]
    players = prop_data["players"]


    for i in range(len(players)):
            player_id = players[i]["id"]
            try: 
                athlete_name = players[i]["first_name"] + " " + players[i]["last_name"]
                league = players[i]["sport_id"]
                if league == "ESPORTS":
                     league =  athlete_name.split(" ")[0]
                     athlete_name = athlete_name.split(" ")[1].lower()
            except KeyError:
                continue

            id_to_name[player_id] = [athlete_name, league]

    for i in range(len(appearances)):
        appearance_id = appearances[i]["id"]
        player_id = appearances[i]["player_id"]
        appearance_to_player_id[appearance_id] = player_id
         

    for i in range(len(over_under_lines)):
        appearance_id = over_under_lines[i]["over_under"]["appearance_stat"]["appearance_id"]
        player_id = appearance_to_player_id[appearance_id]
        
        prop_title = over_under_lines[i]["over_under"]["appearance_stat"]["display_stat"]
        if prop_title in prop_alias:
             prop_title = str(prop_alias[prop_title])

        line = float(over_under_lines[i]["stat_value"])

        props.append(PlayerProp(id_to_name[player_id][0], prop_title, line, id_to_name[player_id][1]))


    return pd.DataFrame([(prop.athleteName, prop.line, prop.propTitle, prop.league) for prop in props], columns=["Name", "Line", "Prop Title", "League"])