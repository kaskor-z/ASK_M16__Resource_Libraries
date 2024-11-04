from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel
from typing import List


app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/user")
async def get_all_users() -> List[User]:
    return users

@app.post("/user/{username}/{age}")
async def create_user(user: User, username: Annotated[str, Path(min_length=5, max_length=20,
                                                                description="Enter username",
                                                                example="little_pony")],
                                        age: int = Path(ge=18, le=120, description="Enter age",
                                                        example="24")) -> str:
    user.id = len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f"User № {user.id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=0, le=100,
                                                   description="Enter User ID", example="1")],
                      username: str = Path(min_length=5, max_length=20,
                                                     description="Enter username", example="little_pony"),
                      age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    try:
        edit_user = next(filter(lambda user: user.id == user_id, users), None)
        edit_user.username = username
        edit_user.age = age
        return f"User {edit_user} updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(ge=0, le=100, description="Enter User ID", example="1")) -> str:
    try:
        edit_user = next(filter(lambda user: user.id == user_id, users), None)
        users.remove(edit_user)
        return f"User with number {user_id} has been deleted from Users DB"
    except ValueError:
        raise HTTPException(status_code=500, detail="Oops! User not found")

