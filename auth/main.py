from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()
security = HTTPBasic()


class User(BaseModel):
    login: str
    password: str
    description: Optional[str] = None


db = list()


def autentification(credentials: HTTPBasicCredentials = Depends(security)):
    if all((credentials.username, credentials.password)):
        for user in db:
            print(credentials.username, credentials.username)
            if user.login == credentials.username and user.password == credentials.password:
                return user
        raise HTTPException(status_code=401, detail="User not register", headers={"WWW-Authenticate": "Basic"})
    else:
        raise HTTPException(status_code=401, detail="Wrong auth data", headers={"WWW-Authenticate": "Basic"})


@app.get("/register")
async def register(username: str, password: str, description: Optional[str] = None):
    user = User(login=username, password=password, description=description)
    if user is not None and user not in db:
        db.append(user)
        print(db)
    elif user in db:
        raise HTTPException(status_code=401, detail="User already exist")
    else:
        raise HTTPException(status_code=401, detail="No user data", )
    return db

@app.get("/login" )
async def login(register_user: User = Depends(autentification)):
    return {"message": "You got my secret, welcome"}