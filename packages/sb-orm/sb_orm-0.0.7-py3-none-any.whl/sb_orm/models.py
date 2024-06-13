from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class TaskStatus(PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    target_url = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    post_body = Column(Text, nullable=True)
    header = Column(Text, nullable=True)
    frequency = Column(Integer, nullable=False)
    times = Column(Integer, nullable=False)
    callback_url = Column(String(255), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    times_completed = Column(Integer, default=0)
    last_result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    def __init__(self, target_url, method, post_body, header, frequency, times, callback_url):
        self.target_url = target_url
        self.method = method
        self.post_body = post_body
        self.header = header
        self.frequency = frequency
        self.times = times
        self.callback_url = callback_url
        self.status = TaskStatus.PENDING
        self.times_completed = 0
        self.last_result = None
        self.error_message = None
        self.completed_at = None
