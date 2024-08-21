from typing import Union
from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel
from random import randrange
from fastapi.middleware.cors import CORSMiddleware
from service import Database

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

db = Database("storage.db")

class Task(BaseModel):
    title: str
    done: bool

@app.get("/tasks")
def get_all_tasks():
    tasks = db.get_all_tasks()
    return {"data": tasks}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    task_dict = db.create_task(task.title, task.done)
    return {"data": task_dict}

@app.delete("/tasks/{id}", status_code=status.HTTP_200_OK)
def delete_task(id: int):
    success = db.delete_task(id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task #{id} doesn't exist")
    return {"message": f"Task #{id} deleted"}

@app.put("/tasks/{id}", status_code=status.HTTP_200_OK)
def update_task(id: int, task: Task):
    updated_task = db.update_task(id, task.title, task.done)
    if updated_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task #{id} doesn't exist")
    return {"data": updated_task}
