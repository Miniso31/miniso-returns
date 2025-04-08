from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os

app = Flask(__name__)

# Connect to Google Sheets via Environment Variable
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.environ.get("GOOGLE_CREDS_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Amazon_Returns_Log").sheet1  # Replace with your actual Google Sheet name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        order_id = request.form.get("order_id", "")
        barcode = request.form.get("barcode", "")
        sku = request.form.get("sku", "")
        condition = request.form.get("condition", "")
        damage_desc = request.form.get("damage_description", "")
        reason = request.form.get("return_reason", "")
        order_date = request.form.get("order_date", "")
        price = request.form.get("price", "")
        lpn = request.form.get("lpn", "")
        box_label = request.form.get("box_label", "")
        warehouse = request.form.get("warehouse", "")
        staff = request.form.get("staff", "")
        platform = request.form.get("platform", "")
        images = ", ".join([f for f in request.form.getlist("images") if f])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet.append_row([
            order_id, barcode, sku, condition, damage_desc, reason, order_date, price,
            lpn, box_label, warehouse, staff, platform, images, timestamp
        ])
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
