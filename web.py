# -*- coding: utf-8 -*-

__author__ = 'Rui'

import importlib
import logging
import datetime

from flask import json, request, Flask
import requests

from database import db_session
from tubeservice import metro_lisboa
from tubeservice.models import LineStatusLog
import settings.config as config

app = Flask(__name__)
app.config.from_object(config)

_backends = {
    'json': {'url': app.config['JSON_BACKEND_URL'], 'module': 'lib.json_backend'},
    'html': {'url': app.config['HTML_BACKEND_URL'], 'module': 'lib.html_backend'},
}

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['GET'])
@app.route("/status/", methods=['GET'])
@app.route("/status/<line>/", methods=['GET'])
def status(line=None):
    active_backend = _backends[app.config['ACTIVE_BACKEND']]
    backend_module = importlib.import_module(active_backend['module'])
    url = active_backend['url']
    metro_lisboa_linestatus = metro_lisboa.LineStatus(requests, backend_module)
    line_status = metro_lisboa_linestatus.get_latest(url, line)

    return json.jsonify(line_status)


@app.route("/status/", methods=["POST"])
def add():
    # Deserialize payload
    data = request.get_json()
    logging.debug(data)
    line_name = data['line']
    status = data['status']
    reason = data['reason']
    timestamp = datetime.datetime.utcfromtimestamp(data['timestamp'])

    # Create db register and write entry in the database
    l = LineStatusLog(line_name, status, reason, timestamp)
    db_session.add(l)
    db_session.commit()

    # HTTP created
    return '', 201


if __name__ == "__main__":
    app.run()









