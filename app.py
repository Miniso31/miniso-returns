import os
import json
import datetime
from flask import Flask, request, render_template, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Setup Google Sheets connection
def get_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.environ.get("GOOGLE_CREDS_JSON")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Amazon_Returns_Log").sheet1
    return sheet

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        barcode = request.form.get('barcode')
        sku = request.form.get('sku')
        condition = request.form.get('condition')
        damage_desc = request.form.get('damage_desc') if condition == 'Damaged' else ''
        return_reason = request.form.get('return_reason')
        order_date = request.form.get('order_date')
        price = request.form.get('price')
        lpn = request.form.get('lpn')
        box_label = request.form.get('box_label')
        warehouse = request.form.get('warehouse')
        staff = request.form.get('staff')
        platform = request.form.get('platform')

        data = [
            order_id, barcode, sku, condition, damage_desc, return_reason,
            order_date, price, lpn, box_label, warehouse, staff, platform,
            str(datetime.datetime.now())
        ]

        sheet = get_gsheet()
        sheet.append_row(data)
        return redirect('/')

    return render_template('index.html')
