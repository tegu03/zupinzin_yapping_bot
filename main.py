# zupinzin_yapping_bot/main.py

import os
import random
import time
import openai
import tweepy
from prompts import tweet_prompt_template
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Setup OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup Twitter (X) API
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_CONSUMER_KEY"),
    os.getenv("TWITTER_CONSUMER_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET"),
)
api = tweepy.API(auth)

# Daftar topik yapping Anoma
TOPICS = [
    "Why Anoma’s intent-centric architecture is revolutionary",
    "Zero-knowledge proofs in Anoma and privacy future",
    "Anoma vs Namada – what's the difference?",
    "How Anoma enables multi-chain coordination",
    "Intent gossiping — what is it really?",
    "Is Anoma really a layer 0?",
    "Decentralized coordination and why it matters",
    "Privacy in crypto is not optional — here’s why",
    "Anoma memes that actually make sense",
]

def generate_tweet(topic: str) -> str:
    prompt = tweet_prompt_template(topic)
    print(f"🧠 Prompting GPT on topic: {topic}")
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or "gpt-4" / "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=280
    )
    
    tweet = response['choices'][0]['message']['content'].strip()
    print(f"✅ Generated Tweet:\n{tweet}\n")
    return tweet

def post_tweet(tweet: str):
    try:
        api.update_status(tweet)
        print("🎉 Tweet posted successfully!")
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")

def main():
    topic = random.choice(TOPICS)
    tweet = generate_tweet(topic)
    post_tweet(tweet)

if __name__ == "__main__":
    main()

