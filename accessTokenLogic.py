import supabaseLogic
import time
import requests
import os


def refreshToken(user_id,refresh_token):
    response = requests.post("https://www.strava.com/oauth/token", data={
        'client_id': os.getenv("CLIENT_ID"),
        'client_secret': os.getenv("CLIENT_SECRET"),
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    })
    return response.json()

def getAccessToken(user_id):
    data=supabaseLogic.get_tokens(user_id)
    #print(data)
    if data["expires_at"]<time.time():
        data=refreshToken(user_id,data["refresh_token"])
        #print("\n\n",data)
        supabaseLogic.save_token(user_id,data["access_token"],data["refresh_token"],data["expires_at"])
        print('token expired')
    else:
        print('token valid\n')
    return data["access_token"]
#print(getAccessToken(112223774))