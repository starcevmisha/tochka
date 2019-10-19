from flask import jsonify
from flask import Flask
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
from worker import celery
import datetime

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

handler = RotatingFileHandler('log.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


from models import *


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fio = request.form['fio']
        balance = request.form['balance']
        balance = balance if balance else 0
        isActive = 'isActive' in request.form
        hold = Hold(fio, isActive, balance)
        db.session.add(hold)
        db.session.commit()

    holds = Hold.query.order_by(Hold.uuid.desc()).all()
    return render_template('index.html', holds=holds)


@app.route("/api/ping", methods=['GET', 'POST'])
def ping():
    return "pong"


@app.route("/api/substract", methods=['GET', 'POST'])
def substract():
    uuid = request.args.get('uuid')
    amount = request.args.get('amount')

    if (not uuid) or (not amount):
        return bad("no args")

    amount = int(amount)
    if amount < 0:
        return bad("amount should be positive number")

    user = Hold.query.filter_by(uuid=uuid).first()
    if user is None:
        return bad("BAD UUID")

    if user.hold + amount > user.balance:
        return bad("not enough money in the account")

    user.hold += amount
    user.last_update = datetime.datetime.now()
    db.session.commit()
    app.logger.info(f'account #{uuid}: hold+={amount}')

    celery.send_task('tasks.substract', args=[uuid, amount], countdown=BaseConfig.SUBSTRACT_TASK_DELAY)

    return ok(user)


@app.route("/api/status", methods=['GET', 'POST'])
def status():
    uuid = request.args.get('uuid')

    if not uuid:
        return bad("no args")

    user = Hold.query.filter_by(uuid=uuid).first()
    if user is None:
        return bad("incorrect UUID")

    return ok(user)


@app.route("/api/add", methods=['GET', 'POST'])
def add():
    uuid = request.args.get('uuid')
    amount = request.args.get('amount')
    if (not uuid) or (not amount):
        return bad("no args")

    amount = int(amount)
    if amount < 0:
        return bad("amount should be positive")

    user = Hold.query.filter_by(uuid=uuid).first()
    if user is None:
        return bad("incorrect UUID")
    if not user.status:
        return bad("account closed")

    user.balance += amount
    user.last_update = datetime.datetime.now()
    db.session.commit()
    app.logger.info(f'account #{uuid}: +{amount}')

    return ok(user)


def bad(description, addition=None):
    return jsonify(Result(status=404, result=False, addition=addition, description=description))


def ok(addition):
    return jsonify(Result(status=200, result=True, addition=addition, description="OK").serialize())


class Result:
    def __init__(self, status=404, result=False, addition=None, description=None):
        self.description = description
        self.addition = addition
        self.result = result
        self.status = status

    def serialize(self):
        return {
            'description': self.description,
            'result': self.result,
            'addition': {
                'fio': self.addition.fio,
                'last_update': self.addition.last_update,
                'created': self.addition.created,
                'balance': self.addition.balance,
                'hold': self.addition.hold,
                'status': "Active" if self.addition.status else "Close",
            } if self.addition is not None else {},
            'status': self.status
        }


if __name__ == '__main__':
    app.run()
