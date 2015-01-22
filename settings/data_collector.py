# -*- coding: utf-8 -*-

__author__ = 'Rui'

from datetime import timedelta

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/Lisbon'

CELERY_BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERYBEAT_SCHEDULE = {
    'get_line_status_every_minute': {
        'task': 'tasks.get_line_status',
        'schedule': timedelta(seconds=60),
    },
}

CELERY_ANNOTATIONS = {
    'tasks.get_line_status': {'rate_limit': '1/m'}
}