# -*- coding: utf-8 -*-

__author__ = 'Rui'

import importlib

from flask import json, Flask
import requests

from lib import metro_lisboa
import settings.web as config

app = Flask(__name__)
app.config.from_object(config)
from tubeservice.models import db

db.init_app(app)

with app.app_context():
    db.create_all()

_backends = {
    'json': {'url': app.config['JSON_BACKEND_URL'], 'module': 'lib.json_backend'},
    'html': {'url': app.config['HTML_BACKEND_URL'], 'module': 'lib.html_backend'},
}

@app.route("/")
@app.route("/status/")
@app.route("/status/<line>/")
def status(line=None):
    active_backend = _backends[app.config['ACTIVE_BACKEND']]
    backend_module = importlib.import_module(active_backend['module'])
    url = active_backend['url']
    metro_lisboa_linestatus = metro_lisboa.LineStatus(requests, backend_module)
    line_status = metro_lisboa_linestatus.get_latest(url, line)

    return json.jsonify(line_status)

if __name__ == "__main__":
    app.run(debug=True)









