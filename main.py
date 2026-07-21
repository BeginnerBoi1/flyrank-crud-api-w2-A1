from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
task_db = [
    {"id": 1, "title": "Buy groceries", "done":False},
    {"id": 2, "title": "Finish week 1", "done":False},
    {"id": 3, "title": "Finish laundry", "done":True}
]

# for adding of task
class TaskCreate(BaseModel):
    title: str

# for the deletion/updating of tasks
class _TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool

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
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
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

# For deleting tasks
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    # Search for the task by its ID
    for index, task in enumerate(task_db):
        if task["id"] == task_id:
            task_db.pop(index)  # Remove task
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    # Raise a 404 error if the task id does not exist
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task with ID {task_id} not found"
    )

# For updating tasks
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, new: _TaskUpdate):
    for task in task_db:
        if task["id"] == task_id:
            # Validate title if supplied
            if new.title is not None:
                if not new.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty.")
                task["title"] = new.title.strip()
            
            if new.done is not None:
                task["done"] = new.done
                
            return task
            
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")