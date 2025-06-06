from dotenv import load_dotenv
load_dotenv()


from flask import Flask, redirect, request, render_template, send_file
import requests
from supabase import create_client

from datetime import datetime, timedelta

import os

#import strava

from supabaseLogic import *
import accessTokenLogic
import strava
import mileCalculations
#import tableDisplay
import matplotlib.pyplot as plt
import io


app = Flask(__name__)


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

print(CLIENT_ID)

@app.route("/")
def index():
    auth_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=activity:read"
    return render_template("index.html", auth_url=auth_url)



@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_response = requests.post("https://www.strava.com/oauth/token", data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    })
    token_data = token_response.json()
    # Save tokens here (for now just print to console)
    print("Access Token:", token_data['access_token'])
    print("Refresh Token:", token_data['refresh_token'])
    save_token(token_data['athlete']['id'],token_data['access_token'],token_data['refresh_token'],token_data['expires_at'],token_data['athlete'] )
    #get_tokens(token_data['athlete']['id'])
    return "Authorization complete! Tokens printed to console. you may close this tab now"

@app.route("/display")
def display():
    # #print(getNumRows())

    # ids = getIds()  #this returns a list of athlete IDs

    # data = []



    # for id in ids:
    #     info = get_tokens(id)
    #     data.append({
    #         "name": info["athlete_firstname"],  # Make sure this key exists
    #         "miles": mileCalculations.get_miles(info['user_id'],datetime(2025,4,1),datetime(2026,1,1))
    #     })


    fig, ax = plt.subplots()
    weeks = list(range(1, 6))
    miles = [3.5, 4.2, 5.1, 4.0, 6.3]
    index=0
    start_date=datetime(2025,4,6)
    while index<9:
        miles[index]=mileCalculations.get_miles(112223774, start_date+timedelta(weeks=index),start_date+timedelta(weeks=index+1))
        index+=1
    ax.bar(weeks, miles)
    ax.set_title("Weekly Mileage")
    ax.set_xlabel("Week")
    ax.set_ylabel("Miles")

    # Save to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return send_file(buf, mimetype="image/png")

    #return render_template("diplay.html", runners_month=_mounthdata,runners_day=day_data)
if __name__ == "__main__":
    app.run(debug=True)
