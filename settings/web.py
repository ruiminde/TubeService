# -*- coding: utf-8 -*-

__author__ = 'Rui'

HTML_BACKEND_URL = "http://app.metrolisboa.pt/status/estado_Linhas.php"
JSON_BACKEND_URL = "http://app.metrolisboa.pt/status/getLinhas.php"
SQLALCHEMY_DATABASE_URI = "sqlite:///tubeservice.db"

# 'json' | 'html'
ACTIVE_BACKEND = 'json'
