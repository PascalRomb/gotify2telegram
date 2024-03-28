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

def send_message_to_telegram(title, body): 
    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(TELEGRAM_BOT_TOKEN, "sendMessage"),
        data={'chat_id': TELEGRAM_NOTIFICATION_ID, 'text': title + "\n\n" + body}
    ).json()
    print("telegram message: " + title + " " + body + " is " + str(response["ok"]))

async def log_push_messages():
    async_gotify = AsyncGotify(
        base_url=NOTIFICATION_SERVER,
        client_token=NOTIFICATION_CLIENT_TOKEN,
    )

    async for msg in async_gotify.stream():
        send_message_to_telegram(msg['title'], msg['message'])

asyncio.run(log_push_messages())
