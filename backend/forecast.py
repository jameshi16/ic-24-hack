import requests
import json

url = "https://dashboard.nixtla.io/api/timegpt"

class Forecaster:
    def __init__(self, data) -> None:
        self.data = data[:97]
        self.new_data = []
        # truncate the last 4 and average every 12
        for i in range(0, len(data), 12):
            self.new_data.append(sum(data[i:i+12])/12)
        print(self.new_data)
    
    def forecast(self):
        dates = ["2015-12-02", "2015-12-03", "2015-12-04", "2015-12-05", "2015-12-06", "2015-12-07", "2015-12-08", "2015-12-09", "2015-12-10"]
        y = {date: value for date, value in zip(dates, self.new_data)}

        payload = {
            "model": "timegpt-1",
            "freq": "D",
            "fh": 3,
            "y": y,
            "clean_ex_first": True,
            "finetune_steps": 0,
            "finetune_loss": "default"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer EUgTS3aD7SHp17xrxLHj2lxV2r43Ti794R6pK02uTvpKu84UsU4ZxvQADblDqrB2FY4hATH9t0rpvPTm3qODqsWQsEeSTgofY3AxuPXKehJddMPT997K7kRu9jgrTvIUIXdW2tRusjmSGELLtGedeKdGs10cpqRDwh0VGesN0Yt7IjdCbcMpHrUfhq9z5xTr8XZrczQYD6ruesKzFG0j4poi48IoFp2xnjjbvCuN8Ii2i14xH69bTUnfAex4LjcC"

        }

        response = requests.post(url, json=payload, headers=headers).json().get("data").get("value")

        return [self.new_data, response]


if __name__ == "__main__":


    forecaster = Forecaster()