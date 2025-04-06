import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.db import database
from routes.todo_resource import todos


@asynccontextmanager
async def lifespan(application: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(todos)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)