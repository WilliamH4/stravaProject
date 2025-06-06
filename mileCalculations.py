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
import accessTokenLogic

access_token = accessTokenLogic.getAccessToken(112223774)

# === Strava API URL to fetch activities ===
url = "https://www.strava.com/api/v3/athlete/activities"

# === Set up request headers ===
headers = {
    "Authorization": f"Bearer {access_token}"
}

# start_date = datetime(2025, 4, 20)
# end_date   = datetime(2026, 1, 1)


# after_timestamp = int(start_date.timestamp())
# before_timestamp= int(end_date.timestamp())

def get_miles(user_id,start_date,end_date):


    if start_date>datetime.now():
        return 0
    elif end_date>datetime.now():
        end_date=datetime.now()


    access_token = accessTokenLogic.getAccessToken(user_id)

    after_timestamp = int(start_date.timestamp())
    before_timestamp= int(end_date.timestamp())


    # === Strava API URL to fetch activities ===
    url = "https://www.strava.com/api/v3/athlete/activities"

    # === Set up request headers ===
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

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

        runs = [activity for activity in data if activity.get("type") == "Run"]

        # print("\n\n")
        # print(len(runs))
        # print("\n\n")

        all_activities.extend(runs)
        page += 1

    #print(type(all_activities))
    #print(all_activities[0])

    total_miles=0

    for run in all_activities:
        total_miles+=run['distance']


    total_miles=total_miles/1609

    print(total_miles)

    return total_miles


# # Calculate miles run since date
# def calculate_march_miles(activities):
#     march_runs = [a for a in activities if a['type'] == 'Run' and is_in_chosen_date_range(a['start_date'])]
#     for run in march_runs:
#         print(run['name'])
#     total_miles = sum(a['distance'] / 1609.34 for a in march_runs)
    
#     print(f"Total runs after choosen date: {len(march_runs)}")
#     print(f"Total miles: {total_miles:.2f}")
    
#     return total_miles

# if __name__ == "__main__":
#     miles = get_miles(112223774,datetime(2025, 5,1),datetime(2026, 1, 1))
#     #calculate_march_miles(activities)
if __name__ == "__main__":
    get_miles(112223774,datetime(2025, 1,1),datetime(2026, 1, 1))
