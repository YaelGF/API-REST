#http Bearer

from urllib import response
from fastapi import FastAPI, HTTPException, status, Depends, Security, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import RedirectResponse

from pydantic import BaseModel

import hashlib

import pyrebase


app = FastAPI()


origins = ["*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebaseConfig = {
    "apiKey": "AIzaSyCqcAsOlCtnuCEmUIUgJJvTeHg9n2xjCg4",
    "authDomain": "loginapirest-b1c29.firebaseapp.com",
    "databaseURL": "https://loginapirest-b1c29-default-rtdb.firebaseio.com/",
    "projectId": "loginapirest-b1c29",
    "storageBucket": "loginapirest-b1c29.appspot.com",
    "messagingSenderId": "364265836121",
    "appId": "1:364265836121:web:09a406b3328d87323f6b48",
    "measurementId": "G-DVS09D026Q"
  };

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()


password_b = hashlib.md5("user".encode())
password = password_b.hexdigest()

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

class Mensaje(BaseModel):
  token:str

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for a user",
    description="Get a token for a user",
    tags=["auth"],
  )
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
      user = credentials.username
      password = credentials.password
      user = auth.sign_in_with_email_and_password(user, password)
      response = {
        "token": user['idToken'],
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.get(
  "/user/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Get a token for a user",
  description="Get a token for a user",
  tags=["auth"],
)
async def get_token_bearer(credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    try:
      user = auth.get_account_info(credentials.credentials)
      uid = user['users'][0]['localId']
      users_data = db.child("users").child(uid).get().val()
      response = {
        "user": users_data,
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.post(
  "/user/",
  summary="Create a new user",
  description="Create a new user",
  tags=["Create"])
async def create_user(email:str,password:str,name:str):
  try:
    user = auth.create_user_with_email_and_password(email, password)
    user = auth.sign_in_with_email_and_password(email, password)
    uid = user['localId']
    print(uid)
    data= {
      "nombre":name,
      "level":"User"
      }
    userData = db.child("users").child(uid).set(data)
    msg = {"token":user['idToken']}
    return msg

  except Exception as e:
    print(f"Error: {e}")