import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from scraperfiles.scraper import startScraper

from tinydb import TinyDB, Query
from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import timedelta

# import pandas as pd

app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173"])
CORS(app)

# Fetches current time and converts to UTS
@app.route('/api/time')
def get_current_time():
    return {'time': int(datetime.now().timestamp())}

# I haven't tested this empirically, but my guess is that the charts use London
# days since Last.fm is based there
london_tz = ZoneInfo("Europe/London")
today_london  = str(datetime.now(london_tz).date())

db = TinyDB('./models/db.json')

# If the data is from yesterday (london), throw it out and start over
dbCheck = Query()
dbList = db.search(dbCheck.date.exists())
if (len(dbList) == 0 or dbList[0]['date'] != today_london):
    db.truncate()
    db.insert({'date': today_london})


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # 1. Ensure file was included
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # 2. Ensure a filename exists
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 3. Save file 
    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        resultDict = startScraper(file_path, UPLOAD_FOLDER, db)

        textOutput = resultDict["output"]
        jsonfile = resultDict["jsonfile"]

        # with open(file_path, 'r') as f:
        #     data = f.read()

        # data = pd.read_csv(file_path)

        return jsonify({"message": "File uploaded successfully!", "filename": file.filename, "content": textOutput, "jsonname": jsonfile})
    # else:
    return jsonify({"error": "Upload failed: incorrect type", "filename": file.filename}), 400


@app.route("/api/<filename>", methods=["GET"])
# If a JSON file with the queried name exists, return its data
def get_json_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    with open(file_path, "r") as f:
        data = json.load(f)

    return jsonify(data)