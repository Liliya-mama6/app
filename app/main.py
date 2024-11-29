from fastapi import FastAPI
from app.routers import user, task

app=FastAPI()


@app.get('/')
def welcome()->dict:
    return {'message':'Welcome to Taskmanager'}


app.include_router(task.router)
app.include_router(user.router1)