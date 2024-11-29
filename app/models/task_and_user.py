from backend.db import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slag = Column(String, unique=True)
    tasks = relationship('Task', back_populates='user')


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    slag = Column(String, unique=True)
    user = relationship('User', back_populates='tasks')
