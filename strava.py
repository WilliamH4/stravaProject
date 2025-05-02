from dotenv import load_dotenv
import os
from flask import Flask, redirect, request, render_template


load_dotenv()  # Loads the .env file

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

#print(CLIENT_ID)

import requests
from datetime import datetime

access_token = "5eefdb1a4e510cb6177aa63dbf9419a35d49c395"

# === Strava API URL to fetch activities ===
url = "https://www.strava.com/api/v3/athlete/activities"

# === Set up request headers ===
headers = {
    "Authorization": f"Bearer {access_token}"
}

start_date = datetime(2025, 1, 1)
end_date   = datetime(2026, 1, 1)


after_timestamp = int(start_date.timestamp())
before_timestamp= int(end_date.timestamp())

def get_recent_activities():
    all_activities = []
    page = 1
    while True:
        params = {
            'per_page': 100,
            'page': page,
            'after':after_timestamp,
            'before':before_timestamp
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Failed to fetch activities:", response.status_code, response.text)
            break
        data = response.json()
        if not data:
            break  # No more activities

        all_activities.extend(data)
        page += 1
    return all_activities

def is_in_chosen_date_range(start_date_str):
    try:
        dt = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return 1#dt.year == 2025 and dt.month >= 0
    except Exception as e:
        print("Date parse error:", e)
        return False

# Calculate miles run since date
def calculate_march_miles(activities):
    march_runs = [a for a in activities if a['type'] == 'Run' and is_in_chosen_date_range(a['start_date'])]
    for run in march_runs:
        print(run['name'])
    total_miles = sum(a['distance'] / 1609.34 for a in march_runs)
    
    print(f"Total runs after choosen date: {len(march_runs)}")
    print(f"Total miles: {total_miles:.2f}")
    
    return total_miles

if __name__ == "__main__":
    activities = get_recent_activities()
    calculate_march_miles(activities)
