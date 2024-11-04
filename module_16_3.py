from fastapi import FastAPI, Path
from typing import Annotated


app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/")
async def get_all_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                                     description="Enter username", example="little_pony")],
                        age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    current_index = str(int(max(users, key=int)) + 1)
    users[current_index] = f"Имя: {username}, возраст: {age}"
    return f"User № {current_index} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example="1")],
                      username: str = Path(min_length=5, max_length=20,
                                                     description="Enter username", example="little_pony"),
                      age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user № {user_id} has been updated"

@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example="1")) -> str:
    if users.get(str(user_id)) == None:
        return f"User number {user_id} is empty! Pls enter valid User ID."
    users.pop(str(user_id))
    return f"User with number {user_id} has been deleted from Users DB"

