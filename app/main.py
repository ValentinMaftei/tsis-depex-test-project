from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
from app.models import Task, TaskCreate, HealthResponse

app = FastAPI(
    title="Task Management API",
    description="A simple API for managing tasks",
    version="1.0.0"
)

# In-memory storage for tasks (for demo purposes)
tasks_db: dict[int, dict] = {}
task_id_counter = 1


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint that returns the status of the API.
    """
    return {
        "status": "healthy",
        "message": "API is running"
    }


@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    """
    Retrieve all tasks.
    Returns a list of all tasks in the system.
    """
    return [
        Task(
            id=task_id,
            title=task["title"],
            description=task["description"],
            completed=task["completed"],
            created_at=task["created_at"]
        )
        for task_id, task in tasks_db.items()
    ]


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """
    Retrieve a specific task by ID.
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    return Task(
        id=task_id,
        title=task["title"],
        description=task["description"],
        completed=task["completed"],
        created_at=task["created_at"]
    )


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    """
    Create a new task.
    """
    global task_id_counter
    
    if not task.title or len(task.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Task title cannot be empty")
    
    task_id = task_id_counter
    task_id_counter += 1
    
    tasks_db[task_id] = {
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": datetime.utcnow()
    }
    
    return Task(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=tasks_db[task_id]["created_at"]
    )


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskCreate):
    """
    Update an existing task.
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task_update.title or len(task_update.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Task title cannot be empty")
    
    tasks_db[task_id]["title"] = task_update.title
    tasks_db[task_id]["description"] = task_update.description
    tasks_db[task_id]["completed"] = task_update.completed
    
    return Task(
        id=task_id,
        title=tasks_db[task_id]["title"],
        description=tasks_db[task_id]["description"],
        completed=tasks_db[task_id]["completed"],
        created_at=tasks_db[task_id]["created_at"]
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    Delete a task by ID.
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    return {"message": "Task deleted successfully!"}
