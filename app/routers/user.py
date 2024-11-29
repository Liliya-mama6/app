from fastapi import APIRouter
from app.backend.db import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.task_and_user import Task


router1=APIRouter(prefix='/user', tags=['user'])


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


@router1.get('/')
def all_users():
    pass


@router1.get('/user_id')
def user_by_id():
    pass


@router1.post('/create')
def create_user():
    pass


@router1.put('/update')
def update_user():
    pass


@router1.delete('/delete')
def delete_user():
    pass