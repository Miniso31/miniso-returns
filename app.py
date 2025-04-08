from flask import Flask, render_template
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread

app = Flask(__name__)

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.environ.get("GOOGLE_CREDS_JSON")

# Convert JSON string to dictionary and create credentials
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your sheet (make sure name matches exactly)
sheet = client.open("Amazon_Returns_Log").sheet1

# --- Flask Routes ---
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
