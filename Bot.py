import requests
import os
import json
import vk_api
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

params = {"access_token": api_key, "v": "5.199", "group_id" : 229129792}
initial_poll = requests.post("https://api.vk.com/method/groups.getLongPollServer", params=params).json()

# print(response.status_code)
# print(response.text)

server = initial_poll['response']['server']
key = initial_poll['response']['key']
ts = initial_poll['response']['ts']

url = f"{server}?act=a_check&key={key}&ts={ts}&wait=25"

# while True:

response = requests.post(url).json()

with open("Latest_response", "w", encoding='utf-8') as f:
    json.dump(response, f, indent=4, ensure_ascii=False)

ts = response['ts']
url = f"{server}?act=a_check&key={key}&ts={ts}&wait=25"

if response['updates'][0]["type"] = "message_new":
    message_info = response['updates'][0]['object']['message']
    with open("Latest_message", "w", encoding='utf-8') as f:
        json.dump(message_info, f, indent=4, ensure_ascii=False)

def process_message(message:dict):
    user_id = message['from_id']

    