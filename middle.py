
from typing import Annotated
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI,Request,HTTPException,status, Body
from fastapi.middleware.cors import CORSMiddleware
import time



app= FastAPI()

user_db={"Teebah":"Big girl"}

class User(BaseModel):
    username:str
    name:str
    email:EmailStr
    password:str
    age:int


@app.middleware("http")
async def request_logger(request:Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration= time.time() - start_time
    log_info = {"Duration": duration, "Request": request.method, "Status": response.status_code}

    print(log_info)

    return response

origins=["http://localhost:8000"]

methods= ["GET","POST","PUT"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],

)



@app.post("/signup",status_code=status.HTTP_201_CREATED)
async def sign_up(user:Annotated[User,Body()]):
    for Id, user_profile in user_db.items():
        if Id == user.username and user_profile["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email and username already exist")
        

    user_db[user.username] = user.model_dump()

    return "Profile Created Successfully"


@app.get("/user",status_code = status.HTTP_200_OK)
async def get_users():
    return user_db

