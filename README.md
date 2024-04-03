[![TeleTok](./img/logo.jpg?raw=true)](https://t.me/TeleTockerBot)

# [TeleTok](https://t.me/TeleTockerBot): Telegram bot for TikTok

## Description

This bot will send you a video from a TikTok. Pretty simple.

Just share a link to the chat (no need to mention the bot)

## Thanks to

Built on top of [aiogram](https://github.com/aiogram/aiogram)

# Installation

## Env

(*REQUIRED*)

- API_TOKEN - Bot token from BotFather 

(*OPTIONAL*)

- ALLOWED_IDS - JSON int list. To give access only to specific user/chat id (default: empty list = all users/chats)

## Local

```bash
$ python3 -m venv venv
$ (venv) pip install -r requirements.txt
$ (venv) echo "API_TOKEN=foo:bar" >> .env
$ (venv) export $(cat .env)
$ (venv) python app
```

## Docker

```bash
$ docker build -t teletok .
$ docker run -e "API_TOKEN=foo:bar" teletok
```

## Compose

```bash
$ echo "API_TOKEN=foo:bar" >> .env
$ docker compose up -d --build
```

# License
MIT

