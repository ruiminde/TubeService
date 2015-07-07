# -*- coding: utf-8 -*-

__author__ = 'Rui'

import importlib
import logging
from datetime import datetime

import requests

import settings.config as config
from tubeservice import metro_lisboa

_backends = {"json": {'url': config.JSON_BACKEND_URL, 'module': "lib.json_backend"},
             "html": {'url': config.HTML_BACKEND_URL, 'module': "lib.html_backend"}}

def get_line_status(active_backend_name):
    active_backend = _backends[active_backend_name]
    backend_module = importlib.import_module(active_backend['module'])
    url = active_backend['url']
    metro_lisboa_lines = metro_lisboa.LineStatus(requests, backend_module)
    metro_lisboa_lines._update_from_remote_site(url)
    logging.warning(metro_lisboa_lines._status)

    for line_name, line_status in metro_lisboa_lines._status.items():
        requests.post('http://localhost:5000/status/',
                      data=dict(line=line_name, status=line_status[0], reason=line_status[1], timestamp=datetime.now()))
