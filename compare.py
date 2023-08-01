from sod_mlb_scrape import scrapeSODLines
from prizepicks_line_scrape import scapePrizePicksLines
from IPython.display import display
import pandas as pd


prizePicksLines = scapePrizePicksLines()
sodLines = scrapeSODLines()
combined_frame = pd.merge(sodLines, prizePicksLines, on=["Name", "Prop Title", "League"])

display(combined_frame.to_string())
