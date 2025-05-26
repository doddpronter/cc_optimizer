import base64
import webbrowser
import json
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import time as tm
load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")

auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={APP_KEY}&redirect_uri=https://127.0.0.1"

def init_tokens(returned_url):
    response_code = f"{returned_url[returned_url.index('code=') + 5: returned_url.index('%40')]}@"
    credentials = f"{APP_KEY}:{APP_SECRET}"
    base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
        "utf-8"
    )

    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "authorization_code",
        "code": response_code,
        "redirect_uri": "https://127.0.0.1",
    }

    init_token_response = requests.post(
            url="https://api.schwabapi.com/v1/oauth/token",
            headers=headers,
            data=payload,
        )

    init_tokens_dict = init_token_response.json()
    data = {"timestamp": datetime.now().isoformat(), "tokens": init_tokens_dict}
    with open("refresh_tokens.txt","w") as f:
        json.dump(data, f)
    return "done!"

def retrieve_tokens(tokens):
    print(f"keys: {tokens.keys()}")
    payload = {
            "grant_type": "refresh_token",
            "refresh_token": tokens['refresh_token'],
        }
    headers = {
        "Authorization": f'Basic {base64.b64encode(f"{APP_KEY}:{APP_SECRET}".encode()).decode()}',
        "Content-Type": "application/x-www-form-urlencoded",
    }

    refresh_token_response = requests.post(
        url="https://api.schwabapi.com/v1/oauth/token",
        headers=headers,
        data=payload,
    )
    data = {"timestamp": datetime.now().isoformat(), "tokens": refresh_token_response.json()}
    with open("refresh_tokens.txt","w") as f:
        json.dump(data, f)
    return "refreshed!"

if __name__ == '__main__':
    if not os.path.exists("refresh_tokens.txt"):
        print(f"path doesn't exist, initializing first tokens")
        webbrowser.open(auth_url)
        returned_url = input("Code from local host: ")
        init_tokens(returned_url)


    with open("refresh_tokens.txt", "r") as f:
        data = json.load(f)
    timestamp = datetime.fromisoformat(data["timestamp"])
    elapsed_time = datetime.now() - timestamp

    if elapsed_time > timedelta(minutes=10):
        print(f"starting up... getting activation tokens")
        retrieve_tokens(data['tokens'])
    
    while True:
        sleep_time = 29*60
        print(f"Sleeping for {sleep_time / 60:.2f} minutes...")
        tm.sleep(sleep_time)
        print(f"refreshing tokens {datetime.now()}")
        retrieve_tokens(data['tokens'])


        
        