from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from IPython.display import display
from helper import decimalToAmerican



url = "https://www.pinnacle.com/en/baseball/mlb/detroit-tigers-vs-miami-marlins/1575835059#player-props"


def scrapePinnacleLine(url):
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    props_dict = {"Name": [], "Prop Title": [], "Line": [], "Over": [], "Under": []}

    WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "matchup-market-groups")))
    props = driver.find_elements(by=By.CLASS_NAME, value="matchup-market-groups")[0].find_elements(by=By.XPATH, value="./child::*")
    for prop in props:

        propInfo = prop.find_elements(By.TAG_NAME, 'span')
        propTitle = propInfo[0].text

        try: 
            overLine = float(propInfo[2].text.split()[1])
            overOdds = float(propInfo[3].text)
            underLine = float(propInfo[4].text.split()[1])
            underOdds = float(propInfo[5].text)
        except IndexError:
            continue

        
        start_paren = propTitle.find("(")
        end_paren =  propTitle.find(")")
        
        #formatting exception, skip prop
        if start_paren == -1 or end_paren == -1:
            continue
        
        
        athlete_name = propTitle[0:start_paren - 1]
        prop = propTitle[start_paren + 1: end_paren]

        props_dict["Name"].append(athlete_name)
        props_dict["Prop Title"].append(prop)
        props_dict["Line"].append(overLine)
        props_dict["Over"].append(decimalToAmerican(overOdds))
        props_dict["Under"].append(decimalToAmerican(underOdds))

    df = pd.DataFrame(props_dict)
    return df

        