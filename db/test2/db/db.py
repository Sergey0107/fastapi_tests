from fastapi import HTTPException
from databases import Database

from config.config import Config, load_config
from models.models import CreateToDoRequest, UpdateToDoRequest, ToDo

config: Config = load_config()
database = Database(config.db_url)


async def create_todo(todo: CreateToDoRequest) -> ToDo:
    query = "INSERT INTO todo_list (title, description, completed) " \
            "VALUES (:title, :description, :completed) RETURNING id;"
    values = {"title": todo.title, "description": todo.description, "completed": False}
    try:
        todo_id = await database.execute(query=query, values=values)
        return ToDo(**todo.model_dump(), id=todo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create todo")


async def get_todo(todo_id: int) -> ToDo:
    query = "SELECT * FROM todo_list WHERE id=:todo_id"
    values = {"todo_id": todo_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch todo from database")
    if result:
        return ToDo(title=result["title"],
                    description=result["description"],
                    completed=result["completed"],
                    id=result["id"])
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


async def update_todo(todo_id: int, todo: UpdateToDoRequest) -> ToDo:
    query = "UPDATE todo_list " \
            "SET title=:title, description=:description, completed=:completed " \
            "WHERE id=:todo_id RETURNING id"
    values = {"title": todo.title,
              "description": todo.description,
              "completed": todo.completed,
              "todo_id": todo_id}
    try:
        result = await database.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update todo in database")
    if result:
        return ToDo(**todo.model_dump(), id=todo_id)
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


async def delete_todo(todo_id: int) -> bool:
    query = "DELETE FROM todo_list WHERE id=:todo_id RETURNING id"
    values = {"todo_id": todo_id}
    try:
        deleted_rows = await database.execute(query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete todo from database")
    if deleted_rows:
        return True
    else:
        raise HTTPException(status_code=404, detail="Todo not found")