from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces import GetUserResponse, ScoreResponse, Task
from all_well import WellnessCalc
from fetch import Fetcher
from nixtlats import TimeGPT
import pandas as pd
from datetime import datetime, timedelta


timegpt = TimeGPT(
    token = 'EUgTS3aD7SHp17xrxLHj2lxV2r43Ti794R6pK02uTvpKu84UsU4ZxvQADblDqrB2FY4hATH9t0rpvPTm3qODqsWQsEeSTgofY3AxuPXKehJddMPT997K7kRu9jgrTvIUIXdW2tRusjmSGELLtGedeKdGs10cpqRDwh0VGesN0Yt7IjdCbcMpHrUfhq9z5xTr8XZrczQYD6ruesKzFG0j4poi48IoFp2xnjjbvCuN8Ii2i14xH69bTUnfAex4LjcC'
)


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


def forecast_scores(scores):
    # take in scores per hours. forecast based on 4 hour intervals
    # average of every 4 hours
    scores = scores[0:97]
    new_scores = []
    for i in range(0, len(scores), 12):
        new_scores.append(sum(scores[i:i+12])/12)

    start_timestamp = datetime(1949, 1, 1)

    # Create a list of timestamps, each 8 hours apart
    timestamps = [start_timestamp + timedelta(hours=12*i) for i in range(len(new_scores))]

    # Create the DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'value': new_scores
    })

    forecasted_values = timegpt.forecast(df)

    print(forecasted_values)

    return forecasted_values



    
def populate_real_data(userid: str):
    fetcher = Fetcher()
    calc = WellnessCalc(fetcher.activity_cleanup(userid),
                        fetcher.sleep_cleanup(userid))
    activity, sleep = calc.get_activity_score(), calc.get_sleep_scores()
    overall = calc.get_overall_score(activity, sleep, 4)

    scores = ScoreResponse(overall, activity, sleep)

    forecasted_scores = calc.forecast_scores()

    return GetUserResponse(userid, calc.start_date, scores)



@app.get("/get_user/{userid}")
def get_user_data(userid: str):
    res = populate_real_data(userid)
    return res

# post endpoint to get json called set-task
@app.post("/set-task")
def set_task(task: dict):
    # create a Task object from the dictionary
    task = Task(**task)
    # return the task object
    return task