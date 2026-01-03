from datetime import datetime
import sys

current_timestamp = int(datetime.now().timestamp())
lastWeek = current_timestamp - 864000

def welcome():
    options = [0,0,0] # [format, fastmode, file1]
    print("Welcome to the Mainstream-O-Matic!\n\nHow do you want to use this program?\n"\
          "1. Export a last.fm user's listening history to a .csv file\n" \
          "2. Manually write your listening history to a .txt file")
    ans1 = input()
    if (ans1 == "1"):        
        print("\nYou've selected .csv input. To get started, follow these steps:\n"\
                "1) Open your browser and go to https://mainstream.ghan.nl/export.html\n" \
                "2) Enter the last.fm username of the user you want to score\n"\
                "3) Select \"Scrobbles\" from the first dropdown and \"csv\" from the second\n"\
                "4) Enter this number in the \"Previous timestamp\" box:", lastWeek, "\n"\
                "5) Click go to download the file, then move it into the same directory as this program\n\n"\
                "Have you completed the above steps?\n1. Yes, run the program\n2. No, I'm not ready")
    elif (ans1 == "2"):
        options[0] = 1
        print("\nYou've selected .txt input. To get started, follow these steps:\n"\
                "1) Use any text editor to create a text file called \"input.txt\" in the same directory as this program\n" \
                "2) On each line, alternate between the artist and how many times you've played them this week\n"\
                "   (they do not have to be in order) For example:\n   Prince\n   34\n   Oasis\n   22\n   etc.\n\n"\
                "Have you completed the above steps?\n1. Yes, run the program\n2. No, I'm not ready")
    ans2 = input()
    if (ans2 != "1"):
        sys.exit("Program exited")

    print("\nDo you want to set a minimum number of plays for an artist to be counted? This will make the program run faster.\n" \
    "1. Yes\n" \
    "2. No")
    ans3 = input()
    if (ans3 == "1"):
        options[1]= 1

    print("\nDo you want to create a .csv file containing more details about the artists?\n" \
    "1. Yes\n" \
    "2. No")
    ans3 = input()
    if (ans3 == "1"):
        options[2]= 1
    
    return options

# print(welcome())