[![TeleTok](./img/logo.jpg?raw=true)](https://t.me/shieldy_bot)

# [TeleTok](https://t.me/TeleTockerBot): Telegram bot for TikTok (and Likee)

Built on top of [aiogram](https://github.com/aiogram/aiogram)

# Installation

## Local

```bash
$ git clone https://github.com/captaincolonelfox/TeleTok
$ python3 -m venv venv
$ (venv) pip install -r requirements.txt
$ (venv) echo "API_TOKEN=foo:bar" >> .env
$ (venv) export $(cat .env)
$ (venv) python main.py
```

## Docker

```bash
$ docker build -t teletok .
$ docker run -e "API_TOKEN=foo:bar" teletok
```


# License
MIT

