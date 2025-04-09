from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Load credentials from Render environment variable
creds_dict = json.loads(os.environ['GOOGLE_CREDS_JSON'])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Connect to the Google Sheet
sheet = client.open("Amazon_Returns_Log").sheet1  # Make sure name matches exactly

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = [
            request.form.get("order_id"),
            request.form.get("barcode"),
            request.form.get("sku"),
            request.form.get("condition"),
            request.form.get("damage_description"),
            request.form.get("return_reason"),
            request.form.get("order_date"),
            request.form.get("price"),
            request.form.get("lpn"),
            request.form.get("box_label"),
            request.form.get("warehouse"),
            request.form.get("staff")
        ]
        try:
            sheet.append_row(data)
            return redirect('/')  # reloads the form after submit
        except Exception as e:
            return f"Error writing to sheet: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
