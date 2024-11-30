from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depence import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.task_and_user import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


from app.backend.db import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


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
def all_users(db: Annotated[Session, Depends(get_db)]):
    result = db.scalar(select(User).where(User.is_activ==True)).all()
    return result


@router1.get('/user_id')
def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    if db.scalar(select(User).where(User.id==user_id, User.is_activ==True)) != None:
        result= db.scalar(select(User).where(User.id==user_id))
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")


@router1.post('/create')
def create_user(db:Annotated[Session, Depends(get_db)], creat_user:CreateUser):
    db.execute(insert(User).values(username=creat_user.username,
                                   firstname=creat_user.firstname,
                                   lastname=creat_user.lastname,
                                   age=creat_user.age,
                                   slag=slugify(creat_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router1.put('/update')
def update_user(db:Annotated[Session, Depends(get_db)], user_id:int, update:UpdateUser):
    anonim=db.scalar(select(User).where(User.id==user_id))
    if anonim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(update(User).where(User.id==user_id).values(
        username=UpdateUser.username,
        firstname=UpdateUser.firstname,
        age=UpdateUser.age,
        lastname=UpdateUser.lastname
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router1.delete('/delete')
def delete_user(db:Annotated[Session, Depends(get_db)], user_id:int, update:UpdateUser):
    anonim = db.scalar(select(User).where(User.id == user_id))
    if anonim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(is_active=False))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
