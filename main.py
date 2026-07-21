from fastapi import FastAPI, HTTPException

app = FastAPI()
task_db = [
    {"id": 1, "title": "Buy groceries", "done":False},
    {"id": 2, "title": "Finish week 1", "done":False},
    {"id": 3, "title": "Finish laundry", "done":True}
]

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