from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class RightSpeechModel(Base):
    __tablename__ = "right_speech"

    id = Column(Integer, primary_key=True)
    message = Column(String)
    truthfulness = Column(Integer)
    kindness = Column(Integer)
    constructiveness = Column(Integer)
    absence_of_false_speech = Column(Integer)
    absence_of_malicious_speech = Column(Integer)
    absence_of_harsh_speech = Column(Integer)
    absence_of_idle_chatter = Column(Integer)
