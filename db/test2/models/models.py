from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    title: str
    description: str


class UpdateToDoRequest(BaseModel):
    title: str
    description: str
    completed: bool = False


class ToDo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False