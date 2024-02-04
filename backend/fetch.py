from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://georgeghetiu:ichack123@cluster0.b1jbmqs.mongodb.net/?retryWrites=true&w=majority"


class Fetcher:
    
    def __init__(self) -> None:
        self.client = MongoClient(uri)

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = self.client["Cluster0"]
        self.sleep_collection = self.db["sleep"]
        self.activity_collection = self.db["activity"]


    def sleep_cleanup(self, user_id):
        documents = self.sleep_collection.find({"_id.user_id": f"{user_id}"})
        transformed_data = {"user_id": None, "durations": []}

        for doc in documents:
            if not transformed_data["user_id"]:
                transformed_data["user_id"] = doc['_id']['user_id']

            sleep_data = doc.get('sleep_durations_data', {}).get('asleep', {})
            light_time = sleep_data.get('duration_light_sleep_state_seconds', 0)
            deep_time = sleep_data.get('duration_deep_sleep_state_seconds', 0)
            rem_time = sleep_data.get('duration_REM_sleep_state_seconds', 0)
            tot_time = sleep_data.get('duration_asleep_state_seconds', 0)
            start_time = doc['metadata']['start_time']

            transformed_data["durations"].append({
                "start_time": start_time,
                "light_time": light_time,
                "deep_time": deep_time,
                "rem_time": rem_time,
                "tot_time": tot_time
            })

        return transformed_data


    def activity_cleanup(self, user_id):
        documents = self.sleep_collection.find({"_id.user_id": f"{user_id}"})

        transformed_data = {"user_id": None, "activities": []}

        for doc in documents:
            if not transformed_data["user_id"]:
                transformed_data["user_id"] = doc['_id']['user_id']

            metadata = doc.get('metadata', {})
            heart_rate_data = doc.get('heart_rate_data', {}).get('summary', {})
            
            start_time = metadata.get('start_time', '')
            end_time = metadata.get('end_time', '')
            avg_hr = heart_rate_data.get('avg_hr_bpm', 100)
            avg_hrv = -1  # Placeholder as this data is not available in the sample
            power = doc.get('power_data', {}).get('avg_watts', 0)
            vo2_max = -1  # Placeholder as this data is not available in the sample

            transformed_data["activities"].append({
                "start_time": start_time,
                "end_time": end_time,
                "avg_hr": avg_hr,
                "avg_hrv": avg_hrv,
                "power": power,
                "vo2_max": vo2_max
            })

        return transformed_data


if __name__ == "__main__":
    fetcher = Fetcher()
    print(fetcher.sleep_cleanup("test1"))
    print(fetcher.activity_cleanup("test1"))