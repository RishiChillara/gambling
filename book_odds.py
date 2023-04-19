from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



url = "https://www.covers.com/sport/basketball/nba/player-props"
driver = webdriver.Firefox()
driver.get(url)


games = driver.find_elements(by=By.CLASS_NAME, value="matchup-cta")
for game in games:
    game.click()
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "player-with-best-odds-card")))
        
    players = driver.find_elements(by=By.CLASS_NAME, value="player-with-best-odds-card")
    for player in players:
        points_scored = driver.find_elements(by=By.ID, value="points-scored-284017-odds-tab").click()
