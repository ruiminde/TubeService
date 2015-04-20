# -*- coding: utf-8 -*-

__author__ = 'Rui'

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class LineStatusLog(Base):
    __tablename__ = 'line_status_log'

    id = Column(Integer, primary_key=True)
    line_name = Column(String(20))
    status = Column(String(20))
    reason = Column(String(512))
    timestamp = Column(DateTime, index=True)

    def __init__(self, line_name, status, reason, timestamp):
        self.line_name = line_name
        self.status = status
        self.reason = reason
        self.timestamp = timestamp

    def __repr__(self):
        return '<LineStatusLog %r %r %r %r>' % (self.id, self.line_name, self.status, self.timestamp)

