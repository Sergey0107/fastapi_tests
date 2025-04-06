import uvicorn
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

DATABASE_URL = 'sqlite:///test02.db'

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "task",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean)
)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)

class TaskSet(BaseModel):
    title: str
    description: str

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}: Application started\n')

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}: Application shutdown\n')

@app.post("/set_task", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(post: TaskSet):
    query = (
        tasks.insert()
        .values(title=post.title, description=post.description, completed=False)
    )
    last_record_id = await database.execute(query=query)
    return {"id": last_record_id, **post.model_dump(), "completed": False}

@app.get('/read_task/{task_id}', response_model=Task)
async def read_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    if res := await database.fetch_one(query=query):
        return res
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Task with id:{task_id} not found'
    )

@app.post('/update_task', response_model=Task)
async def update_task(post: Task):
    query = (
        tasks.update()
        .where(tasks.c.id == post.id)
        .values(title=post.title, description=post.description, completed=post.completed)
    )
    if await database.execute(query=query):
        return {**post.model_dump()}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Task with id:{post.id} not found'
    )

@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    if await database.execute(query):
        return {"detail": f'Task with id: {task_id} deleted'}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Task with id:{task_id} not found'
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)