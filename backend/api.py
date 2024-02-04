from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces import GetUserResponse, ScoreResponse, Task
from all_well import WellnessCalc
from fetch import Fetcher
from scheduling import Scheduler
import json
import numpy as np

app = FastAPI()
n = 8

fetcher = Fetcher()
wellbeings, ids = [], []
for i in range(6):
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


def populate_real_data(userid: str):
    fetcher = Fetcher()
    calc = WellnessCalc(fetcher.activity_cleanup(userid),
                        fetcher.sleep_cleanup(userid))
    activity, sleep = calc.get_activity_score(), calc.get_sleep_scores()
    overall = calc.get_overall_score(activity, sleep, 4)

    scores = ScoreResponse(overall, activity, sleep)

    return GetUserResponse(userid, calc.start_date, scores)

tasks = [{"times": {"start": 5, "end": 7}, "number": [3]}]

@app.get("/get_user/{userid}")
def get_user_data(userid: str):
    res = populate_real_data(userid)
    return res

# post endpoint to get json called set-task
@app.post("/set-task")
def set_task(task: dict):
    # create a Task object from the dictionary
    task = Task(**task)
    assigned = [int(x) for x in scheduler.get_soldier_ids(task.start_hour, task.end_hour, task.number)]
    tasks.append({"times": {"start": task.start_hour, "end": task.end_hour}, "ids": assigned})
    return assigned


@app.get("/tasks")
def get_tasks():
    return tasks