# app.py


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
        hold = Hold(fio)
        db.session.add(hold)
        db.session.commit()

    holds = Hold.query.order_by(Hold.uuid.desc()).all()
    return render_template('index.html', holds=holds)


@app.route("/api/ping")
def ping():
    return "pong"




if __name__ == '__main__':
    app.run()
