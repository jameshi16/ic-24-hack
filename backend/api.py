from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces import GetUserResponse, ScoreResponse, Task
from all_well import WellnessCalc
from fetch import Fetcher
from scheduling import Scheduler
from datetime import datetime
from dateutil import parser
import json
import numpy as np
from forecast import Forecaster
import pickle
import os

app = FastAPI()
n = 8

fetcher = Fetcher()
wellbeings, ids = [], []
for i in range(n):
    calc = WellnessCalc(fetcher.activity_cleanup(f"{i}"),
                        fetcher.sleep_cleanup(f"{i}"))
    activity, sleep = calc.get_activity_score(), calc.get_sleep_scores()
    overall = calc.get_overall_score(activity, sleep, 4)
    wellbeings.append(overall)
    ids.append(i)
dict0 = {"wellbeing": wellbeings, "id": ids}
scheduler = Scheduler(dict0)

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


forecasted_scores = []

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

    global forecasted_values

    forecasted_values.clear()
    
    forecasted_values += forecasted_values['value'].tolist()

    return forecasted_values





def populate_real_data(userid: str):
    fetcher = Fetcher()
    calc = WellnessCalc(fetcher.activity_cleanup(userid),
                        fetcher.sleep_cleanup(userid))
    activity, sleep = calc.get_activity_score(), calc.get_sleep_scores()
    overall = calc.get_overall_score(activity, sleep, 4)

    scores = ScoreResponse(overall, activity, sleep)

    forecast_scores(scores)

    return GetUserResponse(userid, calc.start_date, scores)

# tasks = [{"times": {"end": "2024-02-05T06:00:00+00:00",
#                     "start": "2024-02-04T06:23:06.366000+00:00"}, "ids": [3]}]

@app.get("/get_user/{userid}")
def get_user_data(userid: str):
    res = populate_real_data(userid)
    return res

# post endpoint to get json called set-task
@app.post("/set-task")
def set_task(task: dict):
    tasks = []
    if not os.path.exists('task.cache'):
        with open('task.cache', 'wb') as f:
            pickle.dump([], f)
            f.flush()

    with open('task.cache', 'rb') as f:
        tasks.extend(pickle.load(f))

    # create a Task object from the dictionary
    task = Task(**task)
    start_time = parser.parse(task.start_dt)
    end_time = parser.parse(task.end_dt)
    import random
    assigned = [random.randint(1, n) for _ in range(end_time.hour - start_time.hour)]
    # assigned = [int(x) for x in scheduler.get_soldier_ids(
    #     int(start_time.hour), int(end_time.hour), int(task.number))]
    tasks.append({"times": {"start": start_time, "end": end_time}, "ids": assigned})
    print(tasks)
    with open('task.cache', 'wb') as f:
        pickle.dump(tasks, f)
    return assigned


@app.get("/tasks")
def get_tasks():
    if not os.path.exists('task.cache'):
        with open('task.cache', 'wb') as f:
            pickle.dump([], f)
            f.flush()

    tasks = []
    with open('task.cache', 'rb') as f:
        tasks.extend(pickle.load(f))
    print(tasks)
    return tasks

@app.get("/forecast")
def forecast():
    data = dict0["wellbeing"][0]
    forecaster = Forecaster(data)
    actual, forecast = forecaster.forecast()

    return {"actual":actual, "forecast":forecast}
