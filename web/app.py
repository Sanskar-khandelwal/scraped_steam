from flask import Flask, render_template
import requests
import json
app = Flask(__name__)


@app.route('/')
def index():
    resp = requests.get(
        "http://127.0.0.1:9080/crawl.json?start_requests=true&spider_name=best_selling").json()
    return render_template('index.html', games=resp.get('items'))


if __name__ == '__main__':
    app.run(debug=True)
