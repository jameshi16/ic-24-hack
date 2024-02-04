from datetime import datetime, timedelta

class WellnessCalc:
    def __init__(self, activity_data, sleep_data):
        self.activity_data = activity_data
        self.sleep_data = sleep_data
        self.start_date = self.compute_start_date()

    def compute_start_date(self):
        # Finding the earliest start date from sleep data
        earliest_sleep_start = min(datetime.fromisoformat(duration['start_time']) for duration in self.sleep_data['durations'])
        return earliest_sleep_start.replace(hour=0, minute=0, second=0, microsecond=0)

    def calculate_activity_score(self, avg_hr):
        return avg_hr / 10  # Example normalization

    def get_activity_score(self):
        hourly_scores = [0] * 100  # Initialize a list for 100 hours with scores set to 0
        current_date = self.start_date

        for activity in self.activity_data['activities']:
            start_time = datetime.fromisoformat(activity['start_time'])
            end_time = datetime.fromisoformat(activity['end_time'])

            while start_time < end_time and start_time < current_date + timedelta(hours=100):
                if start_time >= current_date:
                    hour_index = (start_time - current_date).total_seconds() // 3600
                    score = self.calculate_activity_score(activity['avg_hr'])
                    if hour_index < 100:
                        hourly_scores[int(hour_index)] = score
                start_time += timedelta(hours=1)

        return hourly_scores

    def calculate_sleep_score(self, light_time, deep_time, rem_time):
        score = (light_time * 0.25 + deep_time * 0.4 + rem_time * 0.35) / 480 * 10  # Normalize to a scale of 1-10
        return round(score, 1)

    def get_sleep_scores(self):
        hourly_scores = [0] * 100  # Initialize a list for 100 hours with scores set to 0
        current_date = self.start_date

        for duration in self.sleep_data['durations']:
            start_time = datetime.fromisoformat(duration['start_time'])
            end_time = start_time + timedelta(minutes=duration['tot_time'])

            while start_time < end_time and start_time < current_date + timedelta(hours=100):
                if start_time >= current_date:
                    hour_index = (start_time - current_date).total_seconds() // 3600
                    score = self.calculate_sleep_score(duration['light_time'], duration['deep_time'], duration['rem_time'])
                    if hour_index < 100:
                        hourly_scores[int(hour_index)] = score
                start_time += timedelta(hours=1)

        max_score = max(hourly_scores)
        return [round(h / max_score, 1) for h in hourly_scores]

    def get_overall_score(self, activity_scores, sleep_scores, n):
        max_act = max(activity_scores)
        max_sleep = max(sleep_scores)
        combined_scores = [activity / max_act + sleep / max_sleep for activity, sleep in zip(activity_scores, sleep_scores)]

        overall_scores = []
        length = len(combined_scores)
        for i in range(length):
            start = max(0, i - n)
            end = min(length, i + n + 1)
            window_average = sum(combined_scores[start:end]) / (end - start)
            capped_score = min(10, window_average)
            rounded_score = round(capped_score, 1)
            overall_scores.append(rounded_score)

        return overall_scores

# Executing the full class definition with the test data
if __name__ == "__main__":
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

    calculator = WellnessCalc(activity_data, sleep_data)
    activity_scores = calculator.get_activity_score()
    sleep_scores = calculator.get_sleep_scores()

    overall = calculator.get_overall_score(activity_scores, sleep_scores, 4)

    print(activity_scores, sleep_scores)
    print(overall)
