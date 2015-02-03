# -*- coding: utf-8 -*-

__author__ = 'Rui'

import importlib
import logging
from datetime import datetime

import requests
from sqlalchemy.ext.declarative import declarative_base

import settings.config as config
from tubeservice import metro_lisboa
from tubeservice.models import LineStatusLog


Base = declarative_base()

_backends = {
    'json': {'url': config.JSON_BACKEND_URL, 'module': 'lib.json_backend'},
    'html': {'url': config.HTML_BACKEND_URL, 'module': 'lib.html_backend'},
}

from sqlalchemy import create_engine

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()


def get_line_status(active_backend_name):
    active_backend = _backends[active_backend_name]
    backend_module = importlib.import_module(active_backend['module'])
    url = active_backend['url']
    metro_lisboa_lines = metro_lisboa.LineStatus(requests, backend_module)
    metro_lisboa_lines._update_from_remote_site(url)
    logging.warning(metro_lisboa_lines._status)

    # TODO: Get DB context; iterate over all_lines_status; save data
    for line_name, line_status in metro_lisboa_lines._status.items():
        l = LineStatusLog(line_name, line_status[0], line_status[1], datetime.now())
        s.add(l)
        s.commit()
