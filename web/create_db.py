from app import db
from models import *

db.create_all()

hold = Hold('closed account', False)
db.session.add(hold)
db.session.commit()
