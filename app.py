from flask import Flask, render_template, request, redirect
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Load Google credentials from environment variable
creds_dict = json.loads(os.environ['GOOGLE_CREDS_JSON'])

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Open your Google Sheet by name
sheet = client.open("Amazon_Returns_Log").sheet1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        order_id = request.form['order_id']
        barcode = request.form['barcode']
        sku = request.form['sku']
        condition = request.form['condition']
        damage_desc = request.form['damage_desc']
        return_reason = request.form['return_reason']
        order_date = request.form['order_date']
        price = request.form['price']
        lpn = request.form['lpn']
        box_label = request.form['box_label']
        warehouse = request.form['warehouse']
        staff = request.form['staff']
        platform = request.form['platform']

        # Add the data to the Google Sheet
        data = [
            order_id,
            barcode,
            sku,
            condition,
            damage_desc,
            return_reason,
            order_date,
            price,
            lpn,
            box_label,
            warehouse,
            staff,
            platform
        ]
        sheet.append_row(data)
        return redirect('/')
    return render_template('index.html')

# Required for Render to assign the port
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
