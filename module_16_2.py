from fastapi import FastAPI, Path
from typing import Annotated


app = FastAPI()

@app.get("/")
async def my_homepage() -> dict:
    return {"message": "Главная страница"}

@app.get("/user/admin")
async def admin_homepage() -> dict:
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user_homepage(user_id: int = Path(ge=1, le=100, description="Enter User ID", example="33")) -> dict:
    return {"user": {f"Вы вошли как пользователь № {user_id}"}}

@app.get("/user/{user_name}/{user_age}")
async def about_of_user(user_name: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                        user_age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> dict:
    return {"user": {f"Информация о пользователе. Имя: {user_name}, Возраст: {user_age}"}}
