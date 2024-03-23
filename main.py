# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()
task_list = []


class Task(BaseModel):
    task_title: str
    task_description: Optional[str] = None
    task_status: str


@app.get("/")
async def root():
    return {"message": "Started"}

"""
В следующих методах для корректного отображения списка задач, использовался атрибут response_model. 
Он определяет "в каком виде" должен быть результат работы метода.
"""
@app.get("/tasks", response_model=List[Task])
async def tasks():
    return task_list

@app.get("/tasks/{task_id}", response_model=Task)
async def task_by_id(task_id: int):
    if task_id < 0 or task_id >= len(task_list):
        message = {"message": "Invalid id"}
        return JSONResponse(content=message, status_code=200)
    return task_list[task_id]


@app.post("/tasks")
async def add_task(task: Task):
    task_list.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(task_list):
        message = {"message": "Invalid id"}
        return JSONResponse(content=message, status_code=200)
    task_list[task_id] = task
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(task_list):
        message = {"message": "Invalid id"}
        return JSONResponse(content=message, status_code=200)
    task_list.pop(task_id)
    return {"message": f"task {task_id} deleted"}