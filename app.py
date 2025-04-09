from flask import Flask, render_template, request, redirect
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
google_creds = json.loads(os.environ["GOOGLE_CREDS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
client = gspread.authorize(creds)
sheet = client.open("Amazon_Returns_Log").sheet1  # Make sure the name matches exactly

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = [
            request.form.get("order_id", ""),
            request.form.get("barcode", ""),
            request.form.get("sku", ""),
            request.form.get("condition", ""),
            request.form.get("damage_description", ""),
            request.form.get("return_reason", ""),
            request.form.get("order_date", ""),
            request.form.get("price", ""),
            request.form.get("lpn", ""),
            request.form.get("box_label", ""),
            request.form.get("warehouse", ""),
            request.form.get("staff", ""),
        ]
        sheet.append_row(data)
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
