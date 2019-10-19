from app import db
from models import *

db.create_all()

hold = Hold('Старцев Миша', True)
db.session.add(hold)
db.session.commit()
