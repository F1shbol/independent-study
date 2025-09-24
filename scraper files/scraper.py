from linkify import linkifyInput
from frontend import welcome
from formula import getScore, playSearch, addWeight, parseRow3, printBookends, findHeaviest, addGeorge

import pandas as pd
from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame
from time import sleep

# Command to create a single executable
# python -m PyInstaller -F scraper.py

options = welcome()

# gets the lists returned by linkify.py
names, playcounts, links = linkifyInput(options)

frameStarter = {"name": names,
        "playcount": playcounts,}

frame = pd.DataFrame(frameStarter)

# print(frame)

oneweek = []
onemonth = []
threemonths = []
sixmonths = []

idx = 1

for link in links:
    print("running link", idx, "of", len(links)) # progress meter
    ffc_response = requests.get(link) # gets raw code from a site and stores it in a variable
    adp_soup = Soup(ffc_response.text, "html.parser") # turns raw code into a Soup object
    tables = adp_soup.find_all('table') # finds tables in the site
    if (len(tables) < 2):
        print("Error fetching table from link", link)
        idx += 1
        oneweek.append(-1)
        onemonth.append(-1)
        threemonths.append(-1)
        sixmonths.append(-1)
        continue
    adp_table = tables[1] # as the site stands now, the second table is the one with the data we want
    rows = adp_table.find_all('tr') # stores all rows in the table
    list_of_parsed_rows = [parseRow3(row) for row in rows[1:]] # parses every row except the header
    df = DataFrame(list_of_parsed_rows) # turns parsed rows into a pandas dataframe

    lastWeek = df.loc[173:179]
    lastMonth = df.loc[150:179]
    last3Months = df.loc[90:179]

    oneweek.append(round(lastWeek[[1]].mean().iloc[0], 3))
    onemonth.append(round(lastMonth[[1]].mean().iloc[0], 3))
    threemonths.append(round(last3Months[[1]].mean().iloc[0], 3))
    sixmonths.append(round(df[[1]].mean().iloc[0], 3))

    sleep(3)
    idx += 1

frame["1w"] = oneweek
frame["1mo"] = onemonth
frame["3mo"] = threemonths
frame["6mo"] = sixmonths

frame = addWeight(frame) # adds a new column with artists' weighted OWLAs
OWLA = frame['weighted'].sum() / frame['playcount'].sum()

print("\nYour one-week listener average is", round(OWLA, 1), 
      "\nThis means that for each song you played, that many people listened to the artist every day last week")
print("This corresponds to a last.fm mainstream score of approximately ", round(getScore(OWLA), 0), "%", sep="")

frame = frame.sort_values(by='1w')
frame = frame.reset_index() # This adds an extra index column to the left, affecting the iloc calls below
artistList = frame['name'].tolist()
playsList = frame['1w'].tolist()
playSearch(playsList, artistList, len(artistList), OWLA)

printBookends(frame)

frame = addGeorge(frame)
findHeaviest(frame)

leave = 0
while (leave != ""):
    print("Press Enter to exit the program:")
    leave = input()

if (options[2] == 1):
    frame = frame.drop(['weighted', 'LstnrTotal', 'PlayTotal', 'LstnrAvg'], axis=1)
    frame.to_csv('file1.csv')
