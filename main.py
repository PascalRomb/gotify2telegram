import os
import asyncio
import requests
from dotenv import load_dotenv
from gotify import AsyncGotify

load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_NOTIFICATION_ID = os.environ.get("TELEGRAM_NOTIFICATION_ID")
NOTIFICATION_SERVER = os.environ.get("NOTIFICATION_SERVER")
NOTIFICATION_CLIENT_TOKEN = os.environ.get("NOTIFICATION_CLIENT_TOKEN")


assert TELEGRAM_BOT_TOKEN is not None and TELEGRAM_NOTIFICATION_ID is not None and NOTIFICATION_SERVER is not None and NOTIFICATION_CLIENT_TOKEN is not None

        

def convert_string_to_file(body: str):
    return {'document': ('body.txt', body.encode())}

def do_post_request(telegram_method, data, files=None):
    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(TELEGRAM_BOT_TOKEN, telegram_method),
        data=data, files=files
    ).json()
    if(not response['ok']):
        print(response)
    else:
        print("Message successful sent.")

def send_message(message):
    data = {'chat_id': TELEGRAM_NOTIFICATION_ID, 'text': message}
    do_post_request("sendMessage", data)

def send_message_as_file(tile, body):

    files = convert_string_to_file(body)

    data =  {'chat_id': TELEGRAM_NOTIFICATION_ID, 'caption': tile + " [message too long]"}
    do_post_request("sendDocument", data, files)


def send_message_to_telegram(application_name, title, body): 

    title = "[GotifyX" + application_name + "] - " + title
    message = title + "\n\n" + body
    messageLength = len(message)

    if(messageLength >= 4000): # max message length for telegram is 4096, better safe than sorry
        send_message_as_file(title, message)
    else:
        send_message(message)

async def log_push_messages():
    async_gotify = AsyncGotify(
        base_url=NOTIFICATION_SERVER,
        client_token=NOTIFICATION_CLIENT_TOKEN,
    )

    async def get_application_name(app_id):
        applications = await async_gotify.get_applications()
        return next((application['name'] for application in applications if application['id'] == app_id), "")


    async for msg in async_gotify.stream():
        application_name = await get_application_name(msg['appid'])
        send_message_to_telegram(application_name, msg['title'], msg['message'])

asyncio.run(log_push_messages())
