import os

API_TOKEN = os.getenv("API_TOKEN")
USER_ID = int(user_id) if (user_id := os.getenv("USER_ID")) else None
