import requests
from dotenv import load_dotenv
import os

load_dotenv()

def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(telegram_url, data={"chat_id": chat_id, "text": message})
    print(response.status_code)
    print(response.json())