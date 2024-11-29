from fastapi import APIRouter
from app.backend.db import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.task_and_user import User, Task

router=APIRouter(prefix='/task', tags=['task'])


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



@router.get('/')
def all_tasks():
    pass

@router.get('/task_id')
def task_by_id():
    pass


@router.post('/create')
def create_task():
    pass


@router.put('/update')
def update_task():
    pass


@router.delete('/delete')
def delete_task():
    pass