from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_league(league_name):
    league_container = driver.find_element(By.CLASS_NAME, "league-navigation")
    league_list = league_container.find_elements(By.CLASS_NAME, "league")
    for league in league_list:
        name = league.find_element(By.CLASS_NAME, "name")
        if name.text == league_name:
            league.click()
    

#TODO: Make sure to clean up parsed lines
def parse_lines():
    projections = driver.find_elements(by=By.CLASS_NAME, value="projection")
    for projection in projections:
        name = projection.find_element(By.CLASS_NAME, "name")
        line = projection.find_element(By.CLASS_NAME, "score")
        prop = projection.find_element(By.CLASS_NAME, "text")



# may be broken :-)
def prop_navigation(prop_name):
    prop_container = driver.find_element(by=By.CLASS_NAME, value="stat-container")
    prop_categories = prop_container.find_elements(By.CLASS_NAME, value="stat")
    for prop in prop_categories:
        if prop.text == prop_name:            
            prop.click()
 

driver = webdriver.Firefox()
driver.get("https://app.prizepicks.com/board")
WebDriverWait(driver, 2).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "close"))).click()


        


        

    


