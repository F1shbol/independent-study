import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173"])
CORS(app)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

# (Optional) where to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'csv', 'png', 'jpg', 'jpeg', 'gif'}

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
        return jsonify({"message": "File uploaded successfully!", "filename": file.filename})
    # else:
    return jsonify({"error": "Upload failed: incorrect type", "filename": file.filename}), 400