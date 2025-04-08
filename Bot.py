import requests
import os
import json
import vk_api
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DATA = {}

def check_DB_exists():
    try:
        with open("Data_base.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        with open("Data_base.json", 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_DATA, f)
        return DEFAULT_DATA 

def has_DaBlya(text:str) -> bool:
    if "да бля" in text.lower():
        return True
    else:
        return False

def get_user_data(user_id):
    params = {"user_ids" : user_id, "access_token": api_key, "v": "5.199"}

    user = requests.get(f"https://api.vk.com/method/users.get", params=params).json()

    first_name, last_name = user['response'][0]["first_name"], user['response'][0]['last_name']
    return first_name, last_name

def process_message(message:dict) -> bool:
    user_id = str(message['from_id'])
    text = message['text']
    
    if not has_DaBlya(text):
        return False
    
    data = check_DB_exists()

    if not user_id in data:
        first_name, second_name = get_user_data(user_id)
        data[user_id] = {'first_name': first_name, 'second_name': second_name, 'counter': 1}
    else:
        first_name, second_name = data[user_id]['first_name'], data[user_id]['second_name']
        data[user_id]['counter'] += 1

    message = f"Вау, {first_name} {second_name} только что сказал 'да бля'\nВсего он говорил 'да бля' {data[user_id]['counter']} раз."
    vk.messages.send(user_id=user_id, message=message, random_id=0)

    with open('Data_base.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

while True:

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
