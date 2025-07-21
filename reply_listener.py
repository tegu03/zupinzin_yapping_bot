# zupinzin_yapping_bot/reply_listener.py

import os
import openai
import tweepy
import time
from dotenv import load_dotenv
from prompts import reply_prompt_template

# Load .env
load_dotenv()

# Setup OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup Twitter API
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_secret = os.getenv("TWITTER_ACCESS_SECRET")

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

bot_username = os.getenv("BOT_USERNAME")  # Contoh: "zupinzin"

# Simpan ID komentar terakhir agar tidak dobel balas
LAST_REPLY_FILE = "last_reply_id.txt"

def get_last_replied_id():
    if os.path.exists(LAST_REPLY_FILE):
        with open(LAST_REPLY_FILE, 'r') as f:
            return int(f.read().strip())
    return None

def save_last_replied_id(tweet_id):
    with open(LAST_REPLY_FILE, 'w') as f:
        f.write(str(tweet_id))

def generate_reply(comment: str, context: str = "") -> str:
    prompt = reply_prompt_template(comment, context)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.75,
        max_tokens=200
    )
    return response['choices'][0]['message']['content'].strip()

def run_reply_bot():
    print("🤖 Auto-reply bot is running...")
    last_id = get_last_replied_id()
    
    mentions = client.get_users_mentions(
        id=client.get_me().data.id,
        since_id=last_id,
        expansions=["author_id", "in_reply_to_user_id"],
        tweet_fields=["conversation_id"]
    )

    if mentions.data:
        for tweet in reversed(mentions.data):
            tweet_id = tweet.id
            author = tweet.author_id
            text = tweet.text

            if bot_username.lower() in text.lower():
                print(f"💬 New mention: {text}")
                reply_text = generate_reply(comment=text)

                try:
                    client.create_tweet(
                        text=reply_text,
                        in_reply_to_tweet_id=tweet_id
                    )
                    print("✅ Replied:", reply_text)
                    save_last_replied_id(tweet_id)
                except Exception as e:
                    print(f"❌ Failed to reply: {e}")
    else:
        print("🔍 No new mentions.")
    
if __name__ == "__main__":
    while True:
        run_reply_bot()
        time.sleep(60)  # Cek setiap 60 detik

