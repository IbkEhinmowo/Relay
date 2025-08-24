import os
import certifi
from discord.ext import commands
from dotenv import load_dotenv
import discord
import ssl
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
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(reportChannelID)
    if channel:
        await channel.send("fbot is now online and connected!")
    else:
        print(f"Channel with ID {reportChannelID} not found.")
        
        
        
async def send_discord_message(message):
    channel = bot.get_channel(reportChannelID)
    if channel:
        await channel.send(message)
        
        
        


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