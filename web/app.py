# app.py
from flask import abort
from flask import jsonify
from flask import Flask
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

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
        return jsonify(Result(status=404, result=False, description="no args").serialize())
    amount = int(amount)
    if amount < 0:
        return jsonify(Result(status=404, result=False, description="amount should be positive number").serialize())

    user = Hold.query.filter_by(uuid=uuid).first()
    if user is None:
        return jsonify(Result(status=404, result=False, description="BAD UUID").serialize())

    if user.hold + amount > user.balance:
        return jsonify(
            Result(status=404, result=False, addition=user, description="Недостаточно денег на счёте").serialize())

    user.hold += amount
    db.session.commit()
    return jsonify(Result(status=200, result=True, addition=user, description="OK").serialize())


@app.route("/api/status", methods=['GET', 'POST'])
def status():
    uuid = request.args.get('uuid')

    if not uuid:
        return jsonify(Result(status=404, result=False, description="no args").serialize())

    user = Hold.query.filter_by(uuid=uuid).first()
    if user is None:
        return jsonify(Result(status=404, result=False, description="BAD UUID").serialize())

    return jsonify(Result(status=200, result=True, addition=user, description="OK").serialize())


@app.route("/api/add", methods=['POST'])
def add():
    uuid = request.args.get('uuid')
    amount = request.args.get('amount')
    if (not uuid) or (not amount):
        return jsonify(Result(status=404, result=False, description="no args").serialize())
    amount = int(amount)
    if amount < 0:
        return jsonify(Result(status=404, result=False, description="amount < 0").serialize())

    user = Hold.query.filter_by(uuid=uuid).first()
    if user is None:
        return jsonify(Result(status=404, result=False, description="BAD UUID").serialize())

    user.balance += amount
    db.session.commit()
    return jsonify(Result(status=200, result=True, addition=user, description="OK").serialize())


class Result:
    def __init__(self, status=None, result=None, addition=None, description=None):
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
