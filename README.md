# Gotify2Telegram

A simple integration between [Gotify](https://gotify.net) Server and a Telegram Bot.
Can be a useful workaround for ios devices, currently not supported by Gotify notification.



## How to configure
Please use the following docker-compose.yml file in order to run the container:
```yml
version: '3'
services:
  gotify-2-telegram:
    restart: unless-stopped
    image: rhombusthere/gotify2telegram:latest
    volumes:
      - .env:/app/.env
```
Then create a .env file with the following content:
```
TELEGRAM_BOT_TOKEN=<Telegram bot token from BotFather>
TELEGRAM_NOTIFICATION_ID=<telegram bot user chat id>
NOTIFICATION_SERVER=<gotify server ip:port>
NOTIFICATION_CLIENT_TOKEN=<notification client token from gotify>
```
