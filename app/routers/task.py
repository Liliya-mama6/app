from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depence import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.task_and_user import Task, User
from app.schemas import CreatTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

from app.backend.db import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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
def all_tasks(db: Annotated[Session, Depends(get_db)]):
    result = db.scalar(select(Task).where(Task.is_active==True)).all()
    return result

@router.get('/task_id')
def task_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    if db.scalar(select(Task).where(Task.id==user_id)) != None:
        result= db.scalar(select(Task).where(Task.id==user_id))
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")


@router.post('/create')
def create_task(db:Annotated[Session, Depends(get_db)], creat_task:CreatTask, user_id:int):
    anonim = db.scalar(select(User).where(User.id == user_id))
    if anonim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")
    db.execute(insert(Task).values(title=creat_task.title,
                                   content=creat_task.content,
                                   user=anonim,
                                   user_id=anonim.id,
                                   slag=slugify(creat_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
def update_task(db:Annotated[Session, Depends(get_db)], user_id:int, update:UpdateTask):
    anonim=db.scalar(select(Task).where(Task.id==user_id))
    if anonim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(update.where(User.id == user_id).values(
        title=update.title,
        content=update.content
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}



@router.delete('/delete')
def delete_task(db:Annotated[Session, Depends(get_db)], user_id:int, update:UpdateTask):
    anonim = db.scalar(select(Task).where(Task.id == user_id))
    if anonim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(update.where(Task.id == user_id).values(is_active=False))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}


@router.get("/user_id/tasks" )
def tasks_by_user_id(db:Annotated[Session, Depends(get_db)], user_id:int):
    result = db.scalar(select(Task).where(Task.user_id==user_id)).all()
    return result