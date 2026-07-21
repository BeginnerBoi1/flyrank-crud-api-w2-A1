from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
task_db = [
    {"id": 1, "title": "Buy groceries", "done":False},
    {"id": 2, "title": "Finish week 1", "done":False},
    {"id": 3, "title": "Finish laundry", "done":True}
]

# for adding of task
class TaskCreate(BaseModel):
    title: str

@app.get("/")
def get_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health"]
    }

@app.get("/health")
def get_health():
    return {"status": "ok"}

# gets all task
@app.get("/tasks")
def get_all_tasks():  
    return task_db

# gets task by its id
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in task_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# POST A NEW TASK
@app.post("/tasks")
def create_task(task : TaskCreate):
    
    # In case the user enters a blank input
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty!"
        )
    
    next_id = max([t["id"] for t in task_db], default=0) + 1
    
    new_task = {
        "id": next_id,
        "title": task.title.strip(),
        "done": False
    }
    
    task_db.append(new_task)
    return new_task

