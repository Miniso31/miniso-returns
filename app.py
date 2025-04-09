from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render
    app.run(host='0.0.0.0', port=port)        # Bind to 0.0.0.0 to make it public
