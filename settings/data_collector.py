# -*- coding: utf-8 -*-

__author__ = 'Rui'

from datetime import timedelta

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/Lisbon'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERYBEAT_SCHEDULE = {
    'get_line_status_every_minute': {
        'task': 'data_collector.tasks.get_line_status',
        'schedule': timedelta(seconds=60),
    },
}

CELERY_ANNOTATIONS = {
    'data_collector.tasks.get_line_status': {'rate_limit': '1/m'}
}
