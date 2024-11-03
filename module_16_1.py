from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def my_homepage() -> dict:
    return {"message": "Главная страница"}

@app.get("/user/admin")
async def admin_homepage() -> dict:
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user_homepage(user_id: int=999)-> dict:
    return {"user": {f"Вы вошли как пользователь № {user_id}"}}

@app.get("/user/{user_name}/{user_age}")
async def about_of_user(user_name: str="Имя", user_age: int=100) ->dict:
    return {"user": {f"Информация о пользователе. Имя: {user_name}, Возраст: {user_age}"}}
