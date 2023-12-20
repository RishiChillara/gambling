from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from IPython.display import display

from helper import prop_alias
from helper import MLBProps
from helper import calculate_no_vig_percent

import time
import pandas as pd

def odds_export(driver):
    df = scrapeDFSOdds(driver)
    df.to_csv("temp_storage.csv", index=False)
    return df

def scrapeDFSOdds(driver):
    mlb_df = scrapeMLB(driver)
    wnba_df = scrapeDraftKings(driver)

    return pd.concat([mlb_df, wnba_df], ignore_index=True, axis=0)

def scrapeMLB(driver):
    interested_props = ["strikeouts", "earned-runs-allowed","hits-allowed", "walks-allowed", "outs", "singles", "hits", "total-bases", "runs-batted-in"]
    interested_links = []

    for prop in interested_props:
        url = "https://www.scoresandodds.com/mlb/props/" + prop
        driver.get(url)

        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if "prop-bets" in href.split("/"):
                interested_links.append(href)


    interested_links = set(interested_links)
    props_dict = {"Name": [], "Prop Title": [], "Line": [], "Over": [], "Under": [], "League": [], }

    for link in interested_links:
        driver.get(link)
        name = driver.find_element(By.CLASS_NAME, "player-item").text
        try:
            table = driver.find_element(By.CLASS_NAME, "sticky")
        except Exception:
            continue

        for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
            cell_text = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
            if cell_text and cell_text[2] and cell_text[3]:
                    props_dict["Name"].append(name)
                    
                    if cell_text[0] in prop_alias:
                        cell_text[0] = str(prop_alias[cell_text[0]])
                    props_dict["Prop Title"].append(cell_text[0])

                    props_dict["Line"].append(float(cell_text[1]))

                    over_percent, under_percent = calculate_no_vig_percent(int(cell_text[2]), int(cell_text[3]))
                    props_dict["Over"].append(over_percent)
                    props_dict["Under"].append(under_percent)

                    props_dict["League"].append("MLB")


    return pd.DataFrame(props_dict)


def scrapeDraftKings(driver):
    url_to_props = {"https://sportsbook.draftkings.com/leagues/basketball/wnba?category=": ["player-points", "player-rebounds","player-assists"],
                    "https://sportsbook.draftkings.com/leagues/baseball/mlb?category=batter-props&subcategory=": ["total-bases", "hits", "rbis", "hits-+-runs-+-rbis", "strikeouts", "singles"],
                    "https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props&subcategory=": ["strikeouts", "outs-recorded", "hits-recorded", "walks", "earned-runs"]
                    }
    props_dict = {"Name": [], "Prop Title": [], "Line": [], "Over": [], "Under": [], "League": [], }

    for url in url_to_props:  
        for prop in url_to_props[url]:
        
            driver.get(url + prop)

            tables = driver.find_elements(By.CLASS_NAME, "sportsbook-table__body")

            for table in tables:
                for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
                    athelte_name = row.find_element(By.CLASS_NAME, "sportsbook-row-name").text
                    over_odds = 100
                    under_odds = 100
                    line = 0
                    for cell in row.find_elements(By.TAG_NAME, 'td'):
                        line = float(cell.find_element(By.CLASS_NAME, "sportsbook-outcome-cell__line").text)
                        
                        over_or_under = cell.find_element(By.CLASS_NAME, "sportsbook-outcome-cell__label").text
                        odds = cell.find_element(By.CLASS_NAME, "sportsbook-odds").text
                        try: 
                            odds = int(odds)
                        except ValueError:
                            odds = int(odds[1:]) * -1

                        if over_or_under == "O":
                            over_odds = odds
                        else:       
                            under_odds = odds  

                        props_dict["Name"].append(athelte_name)
                        if prop in prop_alias:
                            prop = str(prop_alias[prop])
                        props_dict["Prop Title"].append(prop)
                        props_dict["Line"].append(line)

                        over_percent, under_percent = calculate_no_vig_percent(over_odds, under_odds)
                        props_dict["Over"].append(over_percent)
                        props_dict["Under"].append(under_percent)
                        props_dict["League"].append("WNBA")

    return pd.DataFrame(props_dict)