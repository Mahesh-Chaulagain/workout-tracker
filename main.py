import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GENDER = "Male"
WEIGHT_KG = 65
HEIGHT_CM = 180
AGE = 26

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
SHEET_API_KEY = os.getenv("SHEET_API_KEY")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co"

# for nutritionix data
headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

exercise_param = {
    "query": input("Tell us which exercise did you do:"),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=exercise_param, headers=headers)
result = response.json()


# for using Sheet API
today = datetime.now()

for exercise in result["exercises"]:
    sheet_params = {
        "workout":
        {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    # No Authentication
    # sheet_response = requests.post(
    #     url=f"{sheet_endpoint}/{SHEET_API_KEY}/workoutTracking/workouts",
    #     json=sheet_params
    #     )

    # Basic Authentication
    # sheet_response = requests.post(
    #     url=f"{sheet_endpoint}/{SHEET_API_KEY}/workoutTracking/workouts",
    #     json=sheet_params,
    #     auth=(YOUR USERNAME,YOUR PASSWORD)
    # )

    # Bearer Token Authentication
    bearer_headers = {
        "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
    }

    sheet_response = requests.post(
        url=f"{sheet_endpoint}/{SHEET_API_KEY}/workoutTracking/workouts",
        json=sheet_params,
        headers=bearer_headers,
    )
    print(sheet_response.text)
