from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces import GetUserResponse, ScoreResponse

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return "clueless"

# START: for dummy data until get_user is fully implemented
from datetime import datetime
# END

@app.get("/get_user/{userid}")
def get_user_data(userid: str):
    return GetUserResponse(userid, datetime.utcnow().isoformat(),
                           [ScoreResponse([1, 2, 3],
                                          [1, 2, 3],
                                          [1, 2, 3],
                                          [1, 2, 3])])
