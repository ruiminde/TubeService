# -*- coding: utf-8 -*-

__author__ = 'Rui'

import importlib

from celery import Celery
import requests

import settings.data_collector as config
import settings.web as web_config
from lib import metro_lisboa


app = Celery()
app.config_from_object(config)

_backends = {
    'json': {'url': web_config['JSON_BACKEND_URL'], 'module': 'lib.json_backend'},
    'html': {'url': web_config['HTML_BACKEND_URL'], 'module': 'lib.html_backend'},
}


@app.task
def get_line_status():
    active_backend = _backends[app.config['ACTIVE_BACKEND']]
    backend_module = importlib.import_module(active_backend['module'])
    url = active_backend['url']
    metro_lisboa_linestatus = metro_lisboa.LineStatus(requests, backend_module)
    all_lines_status = metro_lisboa_linestatus.get_latest(url)

    # TODO: Get DB context; iterate over all_lines_status; save data


if __name__ == '__main__':
    app.worker_main()