import requests
import os
import json
import vk_api
from dotenv import load_dotenv

load_dotenv()

def has_DaBlya(text:str) -> bool:
    if "да бля" in text.lower():
        return True
    else:
        return False

def process_message(message:dict) -> bool:
    user_id = message['from_id']
    text = message['text']

    if not has_DaBlya(text):
        return False
    
    
    message = "Вау, ты сказал 'да бля' "
    vk.messages.send(user_id=user_id, message=message, random_id=0)
    return True
    

api_key = os.getenv('API_KEY')

params = {"access_token": api_key, "v": "5.199", "group_id" : 229129792}
initial_poll = requests.post("https://api.vk.com/method/groups.getLongPollServer", params=params).json()

# print(response.status_code)
# print(response.text)

server = initial_poll['response']['server']
key = initial_poll['response']['key']
ts = initial_poll['response']['ts']

url = f"{server}?act=a_check&key={key}&ts={ts}&wait=25"

vk_session = vk_api.VkApi(token=api_key)
vk = vk_session.get_api()

# while True:

response = requests.post(url).json()

with open("Latest_response", "w", encoding='utf-8') as f:
    json.dump(response, f, indent=4, ensure_ascii=False)

ts = response['ts']
url = f"{server}?act=a_check&key={key}&ts={ts}&wait=25"

if response['updates'][0]["type"] == "message_new":
    message_info = response['updates'][0]['object']['message']
    with open("Latest_message", "w", encoding='utf-8') as f:
        json.dump(message_info, f, indent=4, ensure_ascii=False)

    process_message(message_info)



    