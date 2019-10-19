# create_db.py


from app import db
from models import *

db.create_all()

hold = Hold('misha')
db.session.add(hold)
db.session.commit()
