from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from helper import PlayerProp
from helper import mlbPropAlias
from helper import MLBProps
from IPython.display import display

import json 
import pandas as pd



#returns a dataframe with name, line, prop, and league
def scapePrizePicksLines():

    url = "view-source:https://api.prizepicks.com/projections"

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.get(url)

    content = driver.page_source
    content = driver.find_element(By.TAG_NAME, 'pre').text
    parsed_json = json.loads(content)

    prop_dict = {}

    for i in range(len(parsed_json["data"])):
        player_id = parsed_json["data"][i]["relationships"]["new_player"]["data"]["id"]
        propTitle = parsed_json["data"][i]["attributes"]["stat_type"]
        #TODO: Reformat, this is just ugly
        if propTitle in mlbPropAlias:
             propTitle =  mlbPropAlias[propTitle]
        line = parsed_json["data"][i]["attributes"]["line_score"]
        prop_dict[player_id] = PlayerProp(line, propTitle)

    for i in range(len(parsed_json["included"])):
            player_id = parsed_json["included"][i]["id"]
            try: 
                athleteName = parsed_json["included"][i]["attributes"]["name"]
                league = parsed_json["included"][i]["attributes"]["league"]
            except KeyError:
                continue

            prop_dict[player_id].athleteName = athleteName
            prop_dict[player_id].league = league

    return pd.DataFrame([(prop_dict[id].athleteName, prop_dict[id].line, prop_dict[id].propTitle, prop_dict[id].league) for id in prop_dict], columns=["Name", "Line", "Prop Title", "League"])










