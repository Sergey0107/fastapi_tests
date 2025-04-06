from fastapi import FastAPI
from models import UserCreate


app = FastAPI()
users: list[UserCreate] = []

@app.post("/create_user")
async def create_user(new_user: UserCreate):
    users.append(new_user)
    return new_user

@app.get("/showuser")
async def show_users():
    return {"users": users}