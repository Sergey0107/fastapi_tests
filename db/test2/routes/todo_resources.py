from fastapi import APIRouter

from models.models import CreateToDoRequest, UpdateToDoRequest, ToDo
from db.db import create_todo, get_todo, update_todo, delete_todo

todos = APIRouter(prefix="/todos")


@todos.post("/", response_model=ToDo)
async def create(todo: CreateToDoRequest):
    res = await create_todo(todo)
    return res


@todos.get("/{todo_id}", response_model=ToDo)
async def read(todo_id: int):
    res = await get_todo(todo_id)
    return res


@todos.put("/{todo_id}", response_model=ToDo)
async def update(todo_id: int, todo: UpdateToDoRequest):
    res = await update_todo(todo_id, todo)
    return res


@todos.delete("/{todo_id}", response_model=dict)
async def delete(todo_id: int):
    await delete_todo(todo_id)
    return {"message": "Todo deleted successfully"}