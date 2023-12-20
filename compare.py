from odds_scrape import odds_export
from odds_scrape import scrapeMLB
from prizepicks_line_scrape import scapePrizePicksLines
from underdog_line_scrape import scapeUnderDogLines
from parlay_pay_scrape import scrapeParlayPlay
from odds_scrape import scrapeDraftKings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from IPython.display import display
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("--read_odds", default=False, action="store_true",
                    help="Reads odds from last update. Not running with this flag scrapes new data across all leagues")

parser.add_argument("--ud", default=False, action="store_true",
                    help="Underdog Props")

parser.add_argument("--pp", default=False, action="store_true",
                    help="Prizepicks Lines")
parser.add_argument("--esports",default=False, action='store_true', help="just esports")

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

pd.set_option("display.max_colwidth", 10000)


def run():
    args = parser.parse_args()

    if args.esports:
        # underDogLines = scapeUnderDogLines(driver)
        prizePicksLines = scapePrizePicksLines(driver)
        # test_frame = pd.merge(underDogLines, prizePicksLines, on=["Name", "Prop Title"])
        print(prizePicksLines.to_string())
        return

    if args.read_odds:
        sportsbook_lines = pd.read_csv("temp_storage.csv")
        sportsbook_lines['Name'] = sportsbook_lines['Name'].str.strip()
        sportsbook_lines['Prop Title'] = sportsbook_lines['Prop Title'].str.strip()
        sportsbook_lines['League'] = sportsbook_lines['League'].str.strip()
        sportsbook_lines["Line"].apply(lambda x: float(x))
    else:
        sportsbook_lines = odds_export(driver)

    if args.ud:
        dfs_lines = scapeUnderDogLines(driver)
        dfs_winning_line = 0.5495
    if args.pp:
        dfs_lines = scapePrizePicksLines(driver)
        dfs_winning_line = 0.5434
    

    dfs_lines["Line"].apply(lambda x: float(x))

    test_frame = pd.merge(dfs_lines, sportsbook_lines, on=["Name", "Prop Title", "League", "Line"])
    test_frame["Prop Hitting"] = test_frame[["Over", "Under"]].max(axis=1)
    test_frame = test_frame.loc[test_frame['Prop Hitting'] >= dfs_winning_line]
    test_frame = test_frame.sort_values(["Prop Hitting"])


    display(test_frame.to_string())

run()