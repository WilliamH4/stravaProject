from dotenv import load_dotenv
import os
import plotext as plt

#from flask import Flask, redirect, request, render_template


load_dotenv()  # Loads the .env file

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

#print(CLIENT_ID)

import requests
#from datetime import datetime, timedelta
from datetime import *
import accessTokenLogic

access_token = accessTokenLogic.getAccessToken(112223774)

# === Strava API URL to fetch activities ===
url = "https://www.strava.com/api/v3/athlete/activities"

# === Set up request headers ===
headers = {
    "Authorization": f"Bearer {access_token}"
}

start_date = datetime(2025, 4, 6)
end_date   = datetime(2025, 9, 1)


after_timestamp = int(start_date.timestamp())
before_timestamp= int(end_date.timestamp())

def fixed_length(text,length):
    if len(text)<length:
        text=(text+" "*length)
    if len(text)>length:
        text=text[:length]
    return text

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
def calculate_total_miles(activities):
    total_miles = [a for a in activities if a['type'] == 'Run' and is_in_chosen_date_range(a['start_date'])]
    #for run in total_miles:
        #print(run)  print(f"{distance:.2f}")
        #print(fixed_length(run['name'],15),f"{run['distance']/1609.34:.2f}",run['start_date_local'])
    
    print(f"Total runs after choosen date: {len(total_miles)}")
    total_miles = sum(a['distance'] / 1609.34 for a in total_miles)
    print(f"Total miles: {total_miles:.2f}")
    
    return total_miles

def calculate_daily_miles(activities):
    total_miles = [a for a in activities if a['type'] == 'Run' and is_in_chosen_date_range(a['start_date'])]
    days=(end_date-start_date).days
    data=[0]*days
    day=0
    while day<(end_date-start_date).days:
        for run in total_miles:
            run_date= datetime.strptime(run['start_date_local'],"%Y-%m-%dT%H:%M:%SZ")
            if run_date > start_date + timedelta(days=day) and run_date < start_date + timedelta(days=day+1):
                data[day]+=run['distance']/1609.34
        day+=1
    index=0
    days_ran=0
    print("daily totals")
    for date in data:
        if (date!=0):
            days_ran+=1
            print (f"{date:.2f}",fixed_length(str(start_date+timedelta(days=index)),10))
        index+=1
    print("\nran for "+str(days_ran)+" days")

def calculate_weeks(activitys):
    num_weeks = ((end_date - start_date).days) // 7 + 1   
    #print(num_weeks)
    week_data=[0]*num_weeks
    index=0
    week_start=start_date+timedelta(days=1)
    weeks=[0]*num_weeks
    while index<num_weeks:
        weeks[index]=fixed_length(str(start_date+timedelta(weeks= index)),10)
        for activity in activitys:
            run_date=activity['start_date_local']

            if run_date<str(week_start+timedelta(weeks=index+1)) and run_date>str(week_start+timedelta(weeks=index)):
                week_data[index]+=activity['distance']/1609.34
        index+=1
    print("\n")
    print("weekly miles")
    # for week in week_data:
    #     if week !=0:
    #         print(week)
    #plt.theme("default")  
    
    plt.bar(weeks, week_data,marker="█")
    plt.title("miles per week")
    plt.show()




if __name__ == "__main__":
    activities = get_recent_activities()
    calculate_daily_miles(activities)
    calculate_total_miles(activities)
    calculate_weeks(activities)




pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
percentages = [14, 36, 11, 8, 7, 4]

