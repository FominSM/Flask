from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class UserIn(BaseModel):
    name: str
    description: Optional[str] = None


class User(UserIn):
    user_id: int


list_users = [User(user_id=1, name='Pavel'), User(user_id=2, name='Mike')]


@app.get("/users/")
async def show_users():
    return list_users


@app.get("/users/{user_id}")
async def show_user(user_id: int):
    for user in list_users:
        if user.user_id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users/add")
def create_person(attrs: UserIn):
    person = User(user_id=len(list_users)+1, **attrs.dict())
    list_users.append(person)
    return person


@app.put("/users/{user_id}")
async def update_user(user_id: int, attrs: UserIn):
    for user in list_users:
        if user.user_id == user_id:
            user.name = attrs.name
            user.description = attrs.description
            return user
    return HTTPException(status_code=404, detail="User not found")


@app.delete("/users/del/{user_id}")
async def delete_user(user_id: int):
    for user in list_users:
        if user.user_id == user_id:
            list_users.remove(user)
            return list_users
    return {"user_id": user_id}


    

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
