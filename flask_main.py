__author__ = 'Rui'

from flask import Flask
from flask import json
import requests

import metro_lisboa


app = Flask(__name__)

URL = "http://app.metrolisboa.pt/status/estado_Linhas.php"


@app.route("/")
@app.route("/status/")
@app.route("/status/<line>/")
def status(line=None):
    metro_lisboa_linestatus = metro_lisboa.LineStatus(requests)
    status = metro_lisboa_linestatus.get_latest(URL, line)

    return json.jsonify(status)


if __name__ == "__main__":
    app.run(debug=True)