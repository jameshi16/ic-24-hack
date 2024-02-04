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
        self.test_collection = self.db["test"]


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


if __name__ == "__main__":
    mongo_client = MongoUploader()

    
    sleep_nights = mongo_client.generate_sleep('2022-01-01', 7)
    # Inserting transformed data
    user_id = '0'
    mongo_client.insert_needed_sleep(mongo_client.test_collection, user_id, sleep_nights)
