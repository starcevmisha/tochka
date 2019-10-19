import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import BaseConfig

Base = declarative_base()

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))

class Hold(Base):
    __tablename__ = 'holds'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True, nullable=False)
    fio = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    hold = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    last_update = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False)

    def __init__(self):
        self.fio = fio
        self.last_update = datetime.datetime.now()
        self.created = self.last_update
        self.balance = balance
        self.hold = 0
        self.status = status
