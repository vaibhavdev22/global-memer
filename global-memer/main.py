import discord
from discord.ext import tasks, commands
import requests
import random
import os

TOKEN = os.getenv("TOKEN")  # Discord bot token
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Discord channel ID

# Emojis list for random selection
EMOJIS = ["🎉", "✨", "😹", "🌟", "💥", "🔥", "😎", "💫", "😆", "🎭", "🌈", "🐱"]

# Subreddits for cats and other memes
CAT_SUBREDDITS = ["cats", "catmemes", "kitten"]
REGULAR_SUBREDDITS = ["memes", "dankmemes", "funny", "wholesomememes"]

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)


def get_random_reddit_meme():
    # Decide if we are fetching a cat meme or a regular meme
    is_cat = random.choice([True, False])
    if is_cat:
        subreddit = random.choice(CAT_SUBREDDITS)
    else:
        subreddit = random.choice(REGULAR_SUBREDDITS)

    url = f"https://www.reddit.com/r/{subreddit}/random/.json"
    response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})

    if response.status_code == 200:
        try:
            data = response.json()[0]["data"]["children"][0]["data"]
            title = data["title"]
            image_url = data["url"]
            return title, image_url, is_cat
        except Exception as e:
            print(f"Error fetching meme: {e}")
            return "No meme found!", "", is_cat
    else:
        return "Failed to fetch meme.", "", is_cat


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} - Ready to send memes! 🚀")
    meme_task.start()


@tasks.loop(hours=8)
async def meme_task():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        title, url, is_cat = get_random_reddit_meme()

        # Random emoji selection
        emoji1 = random.choice(EMOJIS)
        emoji2 = random.choice(EMOJIS)
        emoji3 = random.choice(EMOJIS)

        # Check if the meme is a cat meme or a regular meme
        if is_cat:
            embed_title = f"🐱 Here’s Your Purr-fect Meme! {emoji1}"
        else:
            embed_title = f"😂 Here's Your Daily LOL! {emoji2}"

        # Create the embedded message
        embed = discord.Embed(
            title=embed_title,
            description=f"**{title}**",
            color=discord.Color.random(),
        )
        embed.add_field(
            name="🌐 Subreddit Source",
            value=f"*This meme is from r/{url.split('/')[4]} subreddit!*",
            inline=False,
        )
        embed.set_image(url=url)
        embed.set_footer(text=f"Brought to you by Desi Memer Bot {emoji3}")

        await channel.send(embed=embed)


bot.run(TOKEN)
