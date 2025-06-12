import os
import time
import requests
from fake_useragent import UserAgent
from telegram import Bot
from telegram.error import TelegramError

# Load environment variables from Replit's .env
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WATCHLIST = os.getenv("WATCHLIST", "").split(",")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # seconds

# Track previously seen stories to avoid duplicates
last_seen_ids = {}

# Set up Telegram bot and UserAgent
bot = Bot(token=TOKEN)
ua = UserAgent()

def check_user(username):
    headers = {'User-Agent': ua.random}
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            user_id = json_data['graphql']['user']['id']
            full_name = json_data['graphql']['user']['full_name']
            profile_pic = json_data['graphql']['user']['profile_pic_url_hd']
            
            if username not in last_seen_ids or last_seen_ids[username] != user_id:
                bot.send_message(chat_id=CHAT_ID, text=f"📸 New update from @{username} ({full_name})")
                bot.send_photo(chat_id=CHAT_ID, photo=profile_pic)
                last_seen_ids[username] = user_id
        else:
            print(f"Failed to fetch {username} (status: {response.status_code})")
    except Exception as e:
        print(f"Error checking {username}: {e}")

def run_bot():
    print("🤖 Bot started and watching Instagram users...")
    while True:
        for username in WATCHLIST:
            check_user(username.strip())
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_bot()
