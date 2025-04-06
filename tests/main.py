import uvicorn

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()


class Contact(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    phone: str


contacts_db: dict[int, Contact] = {}


def id_generator():
    counter = max(contacts_db.keys()) if contacts_db else 0
    while True:
        counter += 1
        yield counter


id_gen = id_generator()


def _check_contact(contact: Contact):
    errors = []
    for db_contact in contacts_db.values():
        if contact.name == db_contact.name:
            errors.append(f"name={contact.name} already taken")
        if contact.email == db_contact.email:
            errors.append(f"email={contact.email} already taken")

    if len(errors) > 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=", ".join(errors))


@app.post("/contacts/", response_model=Contact, status_code=status.HTTP_201_CREATED)
def create_contact(contact: Contact):
    _check_contact(contact)
    contact.id = next(id_gen)
    contacts_db[contact.id] = contact
    return contact


@app.get("/contacts/{id}", response_model=Contact, status_code=status.HTTP_200_OK)
def get_contact(id: int):
    if id not in contacts_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id={id} not found")
    return contacts_db[id]


@app.delete("/contacts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int):
    if id not in contacts_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id={id} not found")
    del contacts_db[id]


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)