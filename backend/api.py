from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces import GetUserResponse, ScoreResponse
from all_well import WellnessCalc

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

# TODO: replace with fetcher class
activity_data = {
    'user_id': 'test1', 
    'activities': [
        {'start_time': '2024-02-02T18:04:04.511000+00:00', 'end_time': '2024-02-03T01:06:04.511000+00:00', 'avg_hr': 62, 'avg_hrv': 40, 'power': 0, 'vo2_max': 50}, 
        {'start_time': '2024-02-03T23:27:26.819000+00:00', 'end_time': '2024-02-04T07:26:26.819000+00:00', 'avg_hr': 71, 'avg_hrv': 35, 'power': 0, 'vo2_max': 55}, 
        {'start_time': '2024-02-03T23:27:55.977000+00:00', 'end_time': '2024-02-04T06:48:55.977000+00:00', 'avg_hr': 70, 'avg_hrv': 42, 'power': 0, 'vo2_max': 60}
    ]
}

sleep_data = {
    'user_id': 'test1', 
    'durations': [
        {'start_time': '2024-02-02T18:04:04.511000+00:00', 'light_time': 196.18959306234333, 'deep_time': 386.7161320329825, 'rem_time': 233.7760460387461, 'tot_time': 328.10009556834797}, 
        {'start_time': '2024-02-03T23:27:26.819000+00:00', 'light_time': 125.92007716252662, 'deep_time': 383.80624773661447, 'rem_time': 304.448456937741, 'tot_time': 99.73084341429514}, 
        {'start_time': '2024-02-04T23:27:55.977000+00:00', 'light_time': 328.0097329042788, 'deep_time': 294.7115028627807, 'rem_time': 314.3028589305899, 'tot_time': 326.41072541539177}
    ]
}

def populate_real_data(userid: str):
    calc = WellnessCalc(activity_data, sleep_data)
    activity, sleep = calc.get_activity_score(), calc.get_sleep_scores()
    overall = calc.get_overall_score(activity, sleep, 4)

    scores = ScoreResponse(overall, activity, sleep)

    return GetUserResponse(userid, calc.start_date, scores)



@app.get("/get_user/{userid}")
def get_user_data(userid: str):
    res = populate_real_data(userid)
    return res
