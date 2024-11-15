from typing import Annotated
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI,Request,HTTPException,status, Body
from fastapi.middleware.cors import CORSMiddleware
import time



app= FastAPI()

user_db={"Toyeebah":{"FirstName":"Teebah", "LastName": "Toyeebah", "email":"tarowona@yahoo.com", "Height":160.2,"age": 20}, "Tope":{"FirstName":"Topie", "LastName": "Tope", "email": "topetee@yahoo.com", "Height":145.2, "age": 55}}

class User(BaseModel):
    FirstName:str
    LastName:str
    email:EmailStr
    height:float
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
        if Id == user.FirstName and user_profile["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email and FirstName already exist")
        

    user_db[user.FirstName] = user.model_dump()

    return "Profile Created Successfully"




