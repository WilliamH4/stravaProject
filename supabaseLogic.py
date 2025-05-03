from dotenv import load_dotenv
load_dotenv()
from supabase import create_client
import os
from flask import Flask, redirect, request, render_template
import requests

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# print("SUPABASE_URL:", url)
# print("SUPABASE_KEY:", key)


supabase = create_client(url, key)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

print(CLIENT_ID)

def save_token(user_id, access_token, refresh_token, expires_at, athlete=" "):
    if (athlete!=" "):
        response = supabase.table('user_tokens').upsert({
            "user_id": user_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
            "athlete_firstname": athlete["firstname"],
            "athlete_lastname": athlete["lastname"],
            "athlete_username": athlete["username"],
            "athlete_profile": athlete["profile"]
        }).execute()
    else:
        response = supabase.table('user_tokens').upsert({
            "user_id": user_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at
        }).execute()


    # if response.status_code != 201 and response.status_code != 200:
    #     print("Error saving tokens:", response.data)
    # else:
    #     print("Tokens saved successfully")

def get_tokens(user_id):
    response = supabase.table("user_tokens").select("*").eq("user_id", user_id).single().execute()
    #print(response.data)
    return response.data

def getNumRows():
    res = supabase.table('user_tokens').select('*', count='exact').execute()
    row_count = res.count
    print(f"Row count: {row_count}")

    return row_count

def getIds():
    response = supabase.table("user_tokens").select("user_id").execute()
    ids = [row["user_id"] for row in response.data]  
    print (ids)
    return ids

#get_tokens(112223774)

#getIds()
#print(getNumRows())