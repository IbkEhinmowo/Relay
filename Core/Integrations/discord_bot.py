print("STARTING BOT")
import os
import certifi
from discord.ext import commands
from dotenv import load_dotenv
import discord
import ssl
import redis
import json

load_dotenv()
import asyncio
from Core.Processor.LLMAGENT import llmagent_process
# SSL fixes for macOS
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()
# Override SSL context globally
ssl._create_default_https_context = ssl._create_unverified_context

BOT_TOKEN = os.getenv("BOT_TOKEN")
reportChannelID = int(os.getenv("DISCORD_REPORT_CHANNEL_ID"))

# Set intents
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content for commands

# Prefix bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event

async def on_ready():
    # print(f'ON_READY: {bot.user} has connected to Discord!')
    channel = bot.get_channel(reportChannelID)
    if channel:
        await channel.send("fbot is now online and connected!")
    else:
        # print(f"Channel with ID {reportChannelID} not found.")
        pass

    # print("ON_READY: Scheduling Redis worker...")
    bot.loop.create_task(redis_message_worker())
        
        
        

async def send_discord_message(message: str):
    channel = bot.get_channel(reportChannelID)
    # print(f"DEBUG: Sending message to channel ID {reportChannelID}: {message}")
    if channel:
        await channel.send(message)
    else:
        # print(f"Channel with ID {reportChannelID} not found.")
        pass

async def redis_message_worker():
    r = redis.Redis(host='localhost', port=6379, db=0)
    await bot.wait_until_ready()
    # print("DEBUG: Redis worker started and waiting for messages...")
    while not bot.is_closed():
        msg_json = r.rpop("discord_queue:default")
    # print(f"DEBUG: Read from Redis: {msg_json}")
        if msg_json:
            try:
                payload = json.loads(msg_json)
                content = payload.get("content")
                # print(f"DEBUG: Decoded payload: {payload}")
                if content:
                    await send_discord_message(content)
            except Exception as e:
                # print(f"Redis worker error: {e}")
                pass
        else:
            await asyncio.sleep(2)
    
    


        
        


@bot.command()
async def hello(ctx):
    await ctx.send("Hiii! I'm Natasha")


# Ask command: collects a user's question, processes it, and replies


@bot.command()
async def ask(ctx):
    await ctx.send("What is your question?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        # Process the question using llmagent_process
        result = llmagent_process(msg.content)
        await ctx.send(result)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)