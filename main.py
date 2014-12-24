__author__ = 'Rui'

from flask import Flask
from metro_lisboa.status import Status
import requests
import json

app = Flask(__name__)

URL = "http://app.metrolisboa.pt/status/estado_Linhas.php"


@app.route("/status")
def status():
    metro_status = Status(requests)
    return json.dumps(metro_status.get_latest(URL))


if __name__ == "__main__":
    app.run()
