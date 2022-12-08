import os
import requests
from datetime import datetime
from dotenv import load_dotenv

GENDER = "male"
WEIGHT_KG = 74.8427
HEIGHT_CM = 68
AGE = 30

load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_AUTH_TOKEN = os.getenv("SHEETY_AUTH_TOKEN")

today = datetime.now()
formatted_date = today.strftime("%m/%d/%Y")
formatted_time = today.strftime("%H:%M:%S")


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell me which exercises you did: ")


headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0",
}

exercise_parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_AUTH_TOKEN}"
}


workout_response = requests.post(exercise_endpoint, json=exercise_parameters, headers=headers)
workout_response.raise_for_status()
result = workout_response.json()

for exercise in result["exercises"]:
    sheety_parameters = {
        "workout": {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": exercise["name"].title(),
            "duration (mins)": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheety_response = requests.post(SHEETY_ENDPOINT, json=sheety_parameters, headers=sheety_headers)
    sheety_response.raise_for_status()
