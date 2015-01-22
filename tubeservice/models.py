# -*- coding: utf-8 -*-

__author__ = 'Rui'

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class LineStatusLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(20))
    status = db.Column(db.String(20))
    reason = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True)

    def __init__(self, line_name, status, reason, timestamp):
        self.line_name = line_name
        self.status = status
        self.reason = reason
        self.timestamp = timestamp

    def __repr__(self):
        return '<LineStatusLog %r %r %r %r>' % (self.id, self.line_name, self.status, self.timestamp)
