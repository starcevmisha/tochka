# models.py


import datetime
from app import db
import sqlalchemy

class Hold(db.Model):
    __tablename__ = 'holds'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False, server_default=sqlalchemy.text("overlay(overlay(md5(random()::text || ':' || clock_timestamp()::text) placing '4' from 13) placing to_hex(floor(random()*(11-8+1) + 8)::int)::text from 17)::cstring"))
    fio = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    hold = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, fio, status=True, balance=0):
        self.fio = fio
        self.last_update = datetime.datetime.now()
        self.created = self.last_update
        self.balance = balance
        self.hold = 0
        self.status = status
