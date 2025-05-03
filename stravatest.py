from dotenv import load_dotenv
load_dotenv()


from flask import Flask, redirect, request, render_template
import requests
from supabase import create_client

import os

#import strava

from supabaseLogic import *
import accessTokenLogic
#import tableDisplay


app = Flask(__name__)


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

print(CLIENT_ID)

@app.route("/")
def index():
    auth_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=activity:read_all"
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
    #print(getNumRows())

    ids=getIds()
    i=0
    data=[]

    for id in ids:
        data[i]=get_tokens(id)
        i+=1




    return render_template("diplay.html",runners=data)

if __name__ == "__main__":
    app.run(debug=True)
