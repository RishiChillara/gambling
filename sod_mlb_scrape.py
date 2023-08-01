from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from IPython.display import display

from helper import mlbPropAlias
from helper import MLBProps
from helper import calculate_no_vig_percent

import time
import pandas as pd

def exportSODLines():
    df = scrapeSODLines()
    df.to_csv("temp_storage.csv", encoding=utf-8, index=False)

def scrapeSODLines():
    interested_props = ["strikeouts", "earned-runs-allowed","hits-allowed", "walks-allowed", "outs", "singles", "hits", "total-bases", "runs-batted-in"]
    interested_links = []

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    for prop in interested_props:
        url = "https://www.scoresandodds.com/mlb/props/" + prop
        driver.get(url)

        allLinks = driver.find_elements(By.TAG_NAME, "a")
        for link in allLinks:
            href = link.get_attribute("href")
            if "prop-bets" in href.split("/"):
                interested_links.append(href)


    interested_links = set(interested_links)
    props_dict = {"Name": [], "Prop Title": [], "Line": [], "Over": [], "Under": [], "League": [], }

    for link in interested_links:
        driver.get(link)
        name = driver.find_element(By.CLASS_NAME, "player-item").text
        

        table = driver.find_element(By.CLASS_NAME, "sticky")
        for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
            cell_text = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
            if cell_text and cell_text[2] and cell_text[3]:
                    props_dict["Name"].append(name)
                    if cell_text[0] in mlbPropAlias:
                        props_dict["Prop Title"].append(mlbPropAlias[cell_text[0]])
                    else: 
                        props_dict["Prop Title"].append(cell_text[0])

                    props_dict["Line"].append(float(cell_text[1]))
                    over_percent, under_percent = calculate_no_vig_percent(int(cell_text[2]), int(cell_text[3]))
                    props_dict["Over"].append(over_percent)
                    props_dict["Under"].append(under_percent)
                    props_dict["League"].append("MLB")


    return pd.DataFrame(props_dict)


            



