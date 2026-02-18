from .linkify import linkifyInput
from .frontend import welcome
from .formula import getScore, playSearch, addWeight, parseRow3, printBookends, findHeaviest, addGeorge

from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame
from time import sleep
import os
from tinydb import TinyDB, Query

# Command to create a single executable
# python -m PyInstaller -F scraper.py

def startScraper(file_path, UPLOAD_FOLDER, db):
    # options = welcome()

    # gets the lists returned by linkify.py
    names, playcounts, links = linkifyInput(file_path)

    textOutput = ""

    frameStarter = {"name": names,
            "playcount": playcounts,}

    frame = pd.DataFrame(frameStarter)

    oneweek = []
    onemonth = []
    threemonths = []
    sixmonths = []

    idx = 1

    for link in links:
        dbCheck = Query()
        dbList = db.search(dbCheck.artist == names[idx-1])
        if (len(dbList) > 0):
            oneweek.append(dbList[0]['x1w'])
            onemonth.append(-1)
            threemonths.append(-1)
            sixmonths.append(-1)
            idx += 1
            continue

        # print("running link", idx, "of", len(links)) # progress meter
        ffc_response = requests.get(link) # gets raw code from a site and stores it in a variable
        adp_soup = Soup(ffc_response.text, "html.parser") # turns raw code into a Soup object
        tables = adp_soup.find_all('table') # finds tables in the site
        if (len(tables) < 2):
            # print("Error fetching table from link", link)
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

        db.insert({'artist': names[idx-1], 'x1w': round(lastWeek[[1]].mean().iloc[0], 3)})

        sleep(3)
        idx += 1

    frame["x1w"] = oneweek
    frame["x1mo"] = onemonth
    frame["x3mo"] = threemonths
    frame["x6mo"] = sixmonths

    frame = addWeight(frame) # adds a new column with artists' weighted OWLAs
    OWLA = frame['weighted'].sum() / frame['playcount'].sum()

    textOutput = "".join([textOutput,"Your one-week listener average is ", str(round(OWLA, 1)), 
        "\nThis means that for each song you played, that many people listened to the artist every day last week"])

    frame = frame.sort_values(by='x1w')
    frame = frame.reset_index() # This adds an extra index column to the left, affecting the iloc calls below
    artistList = frame['name'].tolist()
    playsList = frame['x1w'].tolist()

    templist = [textOutput]
    templist.extend(playSearch(playsList, artistList, len(artistList), OWLA))
    textOutput = "".join(templist)

    templist = [textOutput]
    templist.extend(printBookends(frame))
    textOutput = "".join(templist)

    frame = addGeorge(frame)

    # findHeaviest(frame)
    templist = [textOutput]
    templist.extend(findHeaviest(frame))
    textOutput = "".join(templist)
    
    int_stamp = int(datetime.now().timestamp())
    current_timestamp = str(int_stamp)
    csv_name = current_timestamp + ".csv"
    json_name = current_timestamp + ".json"

    frame = frame.drop(['weighted', 'LstnrTotal', 'PlayTotal', 'LstnrAvg'], axis=1)

    export_path = os.path.join(UPLOAD_FOLDER, csv_name)

    frame.to_csv(export_path)

    export_path2 = os.path.join(UPLOAD_FOLDER, json_name)

    frame.to_json(export_path2, orient='records', compression='infer')

    # return textOutput
    return {
        "output": textOutput,
        "jsonfile": json_name
    }
