from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from helper import PlayerProp
from helper import prop_alias
from IPython.display import display

import json 
import pandas as pd

#returns a dataframe with name, line, prop, and league
def scrapeParlayPlay(driver):

    url = "https://parlayplay.io/"
    driver.get(url)

    props = driver.find_elements(By.CLASS_NAME, "bg-gradient-to-r")


    for prop in props:
        athlete_name = prop.find_element(By.CLASS_NAME, "text-base").text
        esports_prop_title = prop.find_element(By.CLASS_NAME, "text-xs").text
        prop_group = prop.find_elements(By.CLASS_NAME, "w-full")
        line = prop_group[0].text
        prop_title = prop_group[1].text

        print(athlete_name, line, prop_title, esports_prop_title)



    # return pd.DataFrame([(prop.athleteName, prop.line, prop.propTitle, prop.league) for prop in props], columns=["Name", "Line", "Prop Title", "League"])