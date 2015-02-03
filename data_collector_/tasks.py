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


@app.task
def get_line_status():
    active_backend = 'json'
    backend_module = importlib.import_module('lib.json_backend')
    url = "http://app.metrolisboa.pt/status/getLinhas.php"
    metro_lisboa_linestatus = metro_lisboa.LineStatus(requests, backend_module)
    all_lines_status = metro_lisboa_linestatus.get_latest(url)
#    logger.info(all_lines_status)

    # TODO: Get DB context; iterate over all_lines_status; save data


if __name__ == '__main__':
    app.worker_main()
