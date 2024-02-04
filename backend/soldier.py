import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fetch import Fetcher

class Soldier:
    def __init__(self, user_id):
        self.user_id = user_id

        self.fetcher = Fetcher()


    def convert_to_index(self, start_time, seconds):
        start_time = pd.to_datetime(start_time)
        start_hour = start_time.hour
        end_time = start_time + pd.Timedelta(seconds, unit='s')
        end_hour = end_time.hour
        return start_hour, end_hour


    def normalize_scores(self, matrix):
        flat = matrix.flatten()
        minimum = flat.min()
        maximum = flat.max()

        if maximum == minimum:
            # Handle the case where all values are the same
            # Option 1: Return the original matrix
            # return matrix
            # Option 2: Return a matrix of zeros, ones, or any other appropriate value
            return np.zeros(matrix.shape)

        return (matrix - minimum) / (maximum - minimum)


    def generate_sleep_scores(self, data):
        durations = data['durations']
        sleep_scores = [0] * 48  # Initialize list for 24 hours

        for session in durations:
            duration_light_sleep = session["light_time"]
            duration_deep_sleep = session["deep_time"]
            duration_REM_sleep = session["rem_time"]
            # duration_total_sleep = session["tot_time"]
            duration_total_sleep = 28000

            sleep_score = duration_deep_sleep * 0.8 + duration_light_sleep * 0.4 + duration_REM_sleep * 1
            start_hour, end_hour = self.convert_to_index(session['start_time'], duration_total_sleep)
            print(start_hour, end_hour)

            # Distribute the sleep score across the hours of sleep
            for hour in range(start_hour, end_hour + 24):
                # if hour < 24:  # Ensure we don't go beyond the 24-hour range
                sleep_scores[hour] = sleep_score

        # Normalize the sleep scores
        # sleep_scores = self.normalize_scores(sleep_scores)
        
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
            start_hour, end_hour = self.convert_to_index(workout['start_time'], time)
            physical_scores[start_hour:end_hour, i] = physical_score
        # normalize the scores
        physical_scores = self.normalize_scores(physical_scores)
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
            start_hour, end_hour = self.convert_to_index(workout['start_time'], time)
            alertness_scores[start_hour:end_hour, i] = 1-0.6*avg_hrv
        # normalize the scores
        alertness_scores = self.normalize_scores(alertness_scores)
        #take mean of the normalized scores
        alertness_scores = np.mean(alertness_scores, axis=1)
        return alertness_scores


if __name__ == "__main__":
    soldier = Soldier("test1")

    sleep_score = soldier.generate_sleep_scores(soldier.fetcher.sleep_cleanup("test1"))

    print(sleep_score)

