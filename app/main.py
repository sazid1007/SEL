from enum import Enum
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = ""
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium


class Task(TaskBase):
    id: int


tasks: Dict[int, Task] = {}
next_task_id = 1

app = FastAPI(title="Task Management API", version="1.0.0")


@app.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskBase) -> Task:
    global next_task_id
    task = Task(id=next_task_id, **task_data.model_dump())
    tasks[next_task_id] = task
    next_task_id += 1
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskBase) -> Task:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task = Task(id=task_id, **task_data.model_dump())
    tasks[task_id] = task
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
