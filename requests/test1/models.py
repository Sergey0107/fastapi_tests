from pydantic import BaseModel, PositiveInt, Field, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None = Field(default=None, lt=130)
    is_subscribed: bool = False