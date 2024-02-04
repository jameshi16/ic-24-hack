from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import random
from datetime import datetime, timedelta

uri = "mongodb+srv://georgeghetiu:ichack123@cluster0.b1jbmqs.mongodb.net/?retryWrites=true&w=majority"

class MongoUploader:
    def __init__(self) -> None:
        self.client = MongoClient(uri)

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = self.client["Cluster0"]
        self.test_sleep = self.db["test_sleep"]
        self.test_activity = self.db["test_activity"]


    def insert_needed_sleep(self, collection, user_id, sleep_data_list):
        """
        Inserts sleep data for a specific user into the MongoDB collection in a transformed format.

        :param user_id: The user ID for whom the sleep data is being inserted.
        :param sleep_data_list: A list of sleep data dictionaries.
        """
        for sleep_data in sleep_data_list:
            # Transforming each sleep_data dictionary
            transformed_data = {
                "_id": {"user_id": user_id, "start_time": sleep_data.get('start_time')},
                "metadata": {"start_time": sleep_data.get('start_time')},
                "sleep_durations_data": {
                    "asleep": {
                        "duration_light_sleep_state_seconds": sleep_data.get('light_time', 0),
                        "duration_deep_sleep_state_seconds": sleep_data.get('deep_time', 0),
                        "duration_REM_sleep_state_seconds": sleep_data.get('rem_time', 0),
                        "duration_asleep_state_seconds": sleep_data.get('tot_time', 0)
                    }
                }
            }

            # Inserting the transformed data into the collection
            collection.insert_one(transformed_data)
    
    def generate_sleep(self, start_date, days):
        """
        Generates a list of random sleep data entries.

        :param start_date: The starting date for the data entries in 'YYYY-MM-DD' format.
        :param days: The number of days to generate data for.
        :return: A list of sleep data dictionaries.
        """
        sleep_data_list = []
        current_date = datetime.strptime(start_date, '%Y-%m-%d')

        for _ in range(days):
            # Random sleep duration between 7 to 9 hours (in seconds)
            total_sleep_seconds = random.randint(7 * 3600, 9 * 3600)

            # Random distribution of sleep stages
            light_time = random.randint(int(total_sleep_seconds * 0.4), int(total_sleep_seconds * 0.5))
            deep_time = random.randint(int(total_sleep_seconds * 0.2), int(total_sleep_seconds * 0.3))
            rem_time = total_sleep_seconds - light_time - deep_time

            # Random bedtime between 10 PM and 11:59 PM
            bedtime_hour = random.randint(22, 23)
            bedtime_minute = random.randint(0, 59)
            bedtime = current_date.replace(hour=bedtime_hour, minute=bedtime_minute)

            sleep_data = {
                'start_time': bedtime.isoformat(),
                'light_time': light_time,
                'deep_time': deep_time,
                'rem_time': rem_time,
                'tot_time': total_sleep_seconds
            }

            sleep_data_list.append(sleep_data)

            # Increment the date by one day
            current_date += timedelta(days=1)

        return sleep_data_list


    def generate_activity(self, start_date, days, sleep_data):
        """
        Generates a list of random activity data entries, ensuring no overlap with sleep times.

        :param start_date: The starting date for the data entries in 'YYYY-MM-DD' format.
        :param days: The number of days to generate data for.
        :param sleep_data: List of sleep data dictionaries to avoid overlapping with sleep times.
        :return: A list of activity data dictionaries.
        """
        activity_data_list = []
        current_date = datetime.strptime(start_date, '%Y-%m-%d')

        for i in range(days):
            # Get sleep start and end times for the current day
            sleep_start = datetime.fromisoformat(sleep_data[i]['start_time'])
            sleep_end = sleep_start + timedelta(seconds=sleep_data[i]['tot_time'])

            for _ in range(2):  # Two activities per day
                # Generate random start time for the activity
                while True:
                    start_hour = random.randint(0, 21)  # Activity must start before 10 PM
                    start_minute = random.randint(0, 59)
                    activity_start = current_date.replace(hour=start_hour, minute=start_minute)

                    # Activity duration is exactly 2 hours
                    activity_end = activity_start + timedelta(hours=2)

                    # Check for overlap with sleep and other activities
                    if activity_start >= sleep_end or activity_end <= sleep_start:
                        if not any(activity['end_time'] > activity_start.isoformat() and activity['start_time'] < activity_end.isoformat() for activity in activity_data_list):
                            break

                # Randomly generated activity parameters
                avg_hr = random.randint(60, 120)  # Average heart rate
                avg_hrv = random.randint(30, 100)  # Average heart rate variability
                power = random.randint(20, 80)  # Power
                vo2_max = random.randint(30, 60)  # VO2 Max

                activity_data = {
                    'start_time': activity_start.isoformat(),
                    'end_time': activity_end.isoformat(),
                    'avg_hr': avg_hr,
                    'avg_hrv': avg_hrv,
                    'power': power,
                    'vo2_max': vo2_max
                }

                activity_data_list.append(activity_data)

            # Increment the date by one day
            current_date += timedelta(days=1)

        return activity_data_list

    def insert_needed_activity(self, collection, user_id, activity_data_list):
        """
        Inserts activity data for a specific user into the MongoDB collection in a transformed format.

        :param user_id: The user ID for whom the activity data is being inserted.
        :param activity_data_list: A list of activity data dictionaries.
        """
        for activity_data in activity_data_list:
            # Transforming each activity_data dictionary
            transformed_data = {
                "_id": {"user_id": user_id, "start_time": activity_data.get('start_time')},
                "metadata": {
                    "start_time": activity_data.get('start_time'),
                    "end_time": activity_data.get('end_time')
                },
                "heart_rate_data": {"summary": {"avg_hr_bpm": activity_data.get('avg_hr'), "avg_hrv": activity_data.get('avg_hrv'), "vo2_max": activity_data.get('vo2_max')}},
                "power_data": {"avg_watts": activity_data.get('power')}
            }

            # Inserting the transformed data into the collection
            collection.insert_one(transformed_data)

# Example usage
if __name__ == "__main__":
    mongo_client = MongoUploader()

    # Generate and insert sleep data
    sleep_nights = mongo_client.generate_sleep('2022-01-01', 7)
    user_id = '0'
    mongo_client.insert_needed_sleep(mongo_client.test_sleep, user_id, sleep_nights)

    # Generate and insert activity data
    activities = mongo_client.generate_activity('2022-01-01', 7, sleep_nights)
    mongo_client.insert_needed_activity(mongo_client.test_activity, user_id, activities)
