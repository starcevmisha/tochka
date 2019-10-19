from celery import Celery
from config import BaseConfig
from db import Hold, Session
import datetime

celery = Celery('tasks', broker=BaseConfig.CELERY_BROKER_URL, backend=BaseConfig.CELERY_RESULT_BACKEND)


@celery.task(name='tasks.substract')
def substract(uuid : str, amount: int):
    user = Session.query(Hold).filter_by(uuid=uuid).first()
    if user == None:
        return
    user.balance -= amount
    user.hold -= amount
    user.last_update = datetime.datetime.now()
    Session.commit()