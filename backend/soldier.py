import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Soldier:
    def __init__(self, user_id, data):
        self.user_id = user_id
        if data is not None:
            self.sleep_scores = generate_sleep_scores(data)
            self.physical_scores = generate_physical_scores(data)
            # self.alertness_scores = generate_alertness_scores(data)
        else:
            self.sleep_scores = np.zeros(24)
            self.alertness_scores = np.zeros(24)
            self.physical_scores = np.zeros(24)

    def convert_to_index(start_time, seconds):
        start_time = pd.to_datetime(start_time)
        start_hour = start_time.hour
        end_time = start_time + pd.Timedelta(seconds, unit='s')
        end_hour = end_time.hour
        return start_hour, end_hour

    def normalize_scores(matrix):
        flat = matrix.flatten()
        minimum = flat.min()
        maximum = flat.max()
        return (matrix - minimum)/(maximum - minimum)


    def generate_sleep_scores(self, data):
        durations = data['durations']
        sleep_scores = np.zeros((24, len(durations)))
        for i in range(0, len(durations)):
            session = durations[i]
            duration_light_sleep_state_seconds = session["light"]
            duration_deep_sleep_state_seconds = session["deep"]
            duration_REM_sleep_state_seconds = session["REM"]
            duration_total_sleep_state_seconds = session["total"]
            sleep_score = duration_deep_sleep_state_seconds*0.8 + duration_light_sleep_state_seconds*0.4 + duration_REM_sleep_state_seconds*1
            start_hour, end_hour = convert_to_index(session['start_time'], session_total_sleep_state_seconds)
            sleep_scores[start_hour:end_hour, i] = sleep_score

        sleep_scores = normalize_scores(sleep_scores)
        #take mean of the sleep scores
        sleep_scores = np.mean(sleep_scores, axis=1)
        return sleep_scores

    def generate_physical_scores(self, data):
        workouts = data['workouts']
        physical_scores = np.zeros((24, len(workouts)))
        for i in range(0, len(workouts)):
            workout = workouts[i]
            avg_hr = workout['avg_hr']
            energy = workout['energy']
            time = workout['time']
            vo2_max = workout['vo2']
            power = energy/time
            physical_score = power/avg_hr*0.5 + vo2_max*0.5
            start_hour, end_hour = convert_to_index(workout['start_time'], time)
            physical_scores[start_hour:end_hour, i] = physical_score
        # normalize the scores
        physical_scores = normalize_scores(physical_scores)
        #take mean of the normalized scores
        physical_scores = np.mean(physical_scores, axis=1)
        return physical_scores

    def generate_alertness_scores(self, data):
        workouts = data['workouts']
        alertness_scores = np.zeros((24, len(workouts)))
        for i in range(0, len(workouts)):
            workout = workouts[i]
            avg_hrv = workout['avg_hrv']
            time = workout['time']
            start_hour, end_hour = convert_to_index(workout['start_time'], time)
            alertness_scores[start_hour:end_hour, i] = 1-0.6*avg_hrv
        # normalize the scores
        alertness_scores = normalize_scores(alertness_scores)
        #take mean of the normalized scores
        alertness_scores = np.mean(alertness_scores, axis=1)
        return alertness_scores

















