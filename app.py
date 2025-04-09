from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Load Google Credentials from environment variable
google_creds = json.loads(os.environ['GOOGLE_CREDS_JSON'])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
client = gspread.authorize(creds)
sheet = client.open("Amazon_Returns_Log").sheet1  # Must match your actual Google Sheet name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Read form fields
        row = [
            request.form.get("order_id"),
            request.form.get("barcode"),
            request.form.get("sku"),
            request.form.get("condition"),
            request.form.get("damage_desc"),
            request.form.get("return_reason"),
            request.form.get("order_date"),
            request.form.get("price"),
            request.form.get("lpn"),
            request.form.get("box_label"),
            request.form.get("warehouse"),
            request.form.get("staff")
        ]
        # Write to Google Sheet
        sheet.append_row(row)
        return "Return submitted successfully."
    return render_template("index.html")

# WSGI app reference
app = app
