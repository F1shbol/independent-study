import numpy as np
from pandas import DataFrame

# This one takes a row from the html table and extracts
# each date and its number of listeners
def parseRow3(row):
    timeSrch = row.find(attrs={'class':['js-date']})
    time = str(timeSrch.attrs['datetime'])

    listenersSrch = row.find(attrs={'class':['js-value']})
    listeners = int(listenersSrch.attrs['data-value'])

    return time, listeners

def multiplyCells(row):
    return float(row['playcount']) * float(row['1w'])

# Uses multiplyCells above to weight each artist's listener count by their
# playcount, then adds the resulting series to the dataframe as a new column
def addWeight(frame):
    result = frame.apply(multiplyCells, axis=1)
    frame['weighted'] = result
    return frame

# Uses the logarithmic regression of the Pro users' OWLAs and Mainstream scores
# to create an approximate Mainstream score
def getScore(avg):
    result = 12.4619 * np.log(avg) - 67.0731
    return result

# Uses binary search to find the artist whose OWLA is nearest the user's.
# It can't compare the two values it lands between yet, so it only goes down for now
def playSearch(A1, A2, n, Target):
    L = 0
    R = n-1
    while (L<=R):
        m = (L+R)//2
        if (A1[m] < Target):
            L = m + 1
        elif (A1[m] > Target):
            R = m - 1
        else:
            print("You're exactly as mainstream as ", A2[m-1], " (", A1[m-1], " listeners last week)", sep="")
            return
    print("You're about as mainstream as ", A2[m-1], " (", A1[m-1], " listeners last week)\n", sep="")
    return

def printBookends(frame):
    print("Your most mainstream artist was ", frame.loc[len(frame)-1].iloc[1], " (", frame.loc[len(frame)-1].iloc[3], 
      " average listeners last week)", sep="")
    print("Your most obscure artist was ", frame.loc[0].iloc[1], " (", frame.loc[0].iloc[3], 
      " average listeners last week)\n", sep="")

def totalListenersColumn(frame):
    lst = []
    for i in range(len(frame)):
        lst.append(frame['weighted'].sum())
    frame['LstnrTotal'] = lst
    return frame

def totalPlaysColumn(frame):
    lst = []
    for i in range(len(frame)):
        lst.append(frame['playcount'].sum())
    frame['PlayTotal'] = lst
    return frame

def avgListenersColumn(frame):
    lst = []
    for i in range(len(frame)):
        lst.append(frame['weighted'].sum() / frame['playcount'].sum())
    frame['LstnrAvg'] = lst
    return frame

def georgeBailey(row):
    # return float(row['playcount']) * float(row['1w'])
    clarence = (row['LstnrTotal'] - row['weighted']) / (row['PlayTotal'] - row['playcount'])
    return row['LstnrAvg'] - clarence

def addGeorge(frame):
    totalListenersColumn(frame)
    totalPlaysColumn(frame)
    avgListenersColumn(frame)

    result = frame.apply(georgeBailey, axis=1)
    frame['impact'] = result
    return frame

def findHeaviest(df):
    print("Your favorite mainstream artist was ", df.loc[df['impact'].idxmax()].iloc[1], ", which you played ",
          df.loc[df['impact'].idxmax()].iloc[2], " times", sep="")
    print("Your favorite obscure artist was ", df.loc[df['impact'].idxmin()].iloc[1], ", which you played ",
          df.loc[df['impact'].idxmin()].iloc[2], " times", sep="")