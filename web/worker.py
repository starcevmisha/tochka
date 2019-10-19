from celery import Celery
from config import BaseConfig

celery = Celery('tasks', broker=BaseConfig.CELERY_BROKER_URL, backend=BaseConfig.CELERY_RESULT_BACKEND)