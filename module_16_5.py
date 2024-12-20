from fastapi import FastAPI, Path, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int


class UserNotFound(Exception):
    def __init__(self, err_message, add_info):
        self.err_message = err_message
        self.add_info = add_info


@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get(path="/user/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        user = next(filter(lambda user: user.id == user_id, users), None)
        if user == None:
            raise UserNotFound("*** ERROR GET *** Oops! User can't will be getting from DB. User not found",
                               f" --> add information: user_id = {user_id} --> list users size = {len(users)}")
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except UserNotFound as UNF_:
        print(f"ERROR: status cod = 410  {UNF_.err_message}")
        return HTTPException(status_code=410, detail=UNF_.err_message + UNF_.add_info)

@app.post("/user/{username}/{age}")
async def create_user(user: User, username: Annotated[str, Path(min_length=5, max_length=20,
                                                                description="Enter username",
                                                                example="User_0")],
                                        age: int = Path(ge=18, le=120, description="Enter age",
                                                        example="24")) -> str:
    if users:
         user_id = max(users, key=lambda m: m.id).id + 1
    else:
         user_id = 1
    user.id = user_id
    user.username = username
    user.age = age
    users.append(user)
    return f"User {username} № {user_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=0, le=100,
                                                   description="Enter User ID", example="1")],
                      username: str = Path(min_length=5, max_length=20,
                                                     description="Enter username", example="little_pony"),
                      age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    try:
        edit_user = next(filter(lambda user: user.id == user_id, users), None)
        if edit_user == None:
            raise UserNotFound("*** ERROR UPDATE *** Oops! User can't be updated to DB. User not found",
                               f" --> add information: user_id = {user_id} --> list users size = {len(users)}")
        edit_user.username = username
        edit_user.age = age
        return f"User {edit_user} updated!"
    except UserNotFound as UNF_:
        print(f"ERROR: status cod = 410  {UNF_.err_message}")
        raise HTTPException(status_code=410, detail=UNF_.err_message + UNF_.add_info)

@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(ge=0, le=100, description="Enter User ID", example="1")) -> str:
    try:
        edit_user = next(filter(lambda user: user.id == user_id, users), None)
        if edit_user == None:
            raise UserNotFound("*** ERROR DELETE *** Oops! User can't be removed from DB. User not found",
                               f" --> add information: user_id = {user_id} --> list users size = {len(users)}")
        users.remove(edit_user)
        return f"User with number {user_id} has been deleted from Users DB"
    except UserNotFound as UNF_:
        print(f"ERROR: status cod = 410  {UNF_.err_message}")
        raise HTTPException(status_code=410, detail=UNF_.err_message + UNF_.add_info)
