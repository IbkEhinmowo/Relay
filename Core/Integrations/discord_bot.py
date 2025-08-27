print("STARTING BOT")
import os
import certifi
from discord.ext import commands
import discord
import ssl
import redis
import json
import asyncio
from Core.Processor.LLMAGENT import llmagent_process
from Core.inputAdapters.DiscordInputEvent import DiscordInputEvent
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
    if channel:
        async with channel.typing():
            await channel.send(message)
    else:
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
    await ctx.trigger_typing()
    await ctx.send("Hiii! I'm Natasha")


# Ask command: collects a user's question, processes it, and replies


@bot.command()
async def ask(ctx):

    async with ctx.typing():
        await ctx.send("What is your question?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        async with ctx.typing():
            # Use DiscordInputEvent to standardize input
            quoted_content = None
            if msg.reference and msg.reference.resolved:
                quoted_content = msg.reference.resolved.content
            event = DiscordInputEvent(
                user_id=str(msg.author.id),
                content=msg.content,
                username=msg.author.display_name,
                quoted_content=quoted_content
            )
            result = await llmagent_process(event.to_prompt())
            await ctx.send(result)
    except asyncio.TimeoutError:
        async with ctx.typing():
            await ctx.send("You took too long to respond!")


# Respond to @bot mentions also 
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Redis connection for chat context (db=1)
    chat_redis = redis.Redis(host='localhost', port=6379, db=1)
    channel_id = str(message.channel.id)
    # Store both username and message content
    msg_text = json.dumps({"username": message.author.display_name, "content": message.content})
    redis_key = f"channel:{channel_id}:history"
    # Add message to channel's history (right push)
    chat_redis.rpush(redis_key, msg_text)
    # Trim to last 30 messages
    chat_redis.ltrim(redis_key, -30, -1)

    # Check if the bot is mentioned (official Discord mention)
    if bot.user in message.mentions:
        async with message.channel.typing():
            quoted_content = None
            # If replying to a message, get the original content
            if message.reference and message.reference.resolved:
                quoted_content = message.reference.resolved.content
            # Get channel message history (excluding current message)
            history = chat_redis.lrange(redis_key, 0, -2)  # All except last (current)
            # Decode bytes to str and format as "username: content"
            message_history = []
            for h in history:
                try:
                    msg_obj = json.loads(h.decode('utf-8'))
                    formatted = f"{msg_obj.get('username', 'Unknown')}: {msg_obj.get('content', '')}"
                except Exception:
                    formatted = h.decode('utf-8')
                message_history.append(formatted)
            event = DiscordInputEvent(
                user_id=str(message.author.id),
                content=message.content,
                username=message.author.display_name,
                quoted_content=quoted_content,
                message_history=message_history
            )
            
            try:
                print (event.to_prompt())
                result = await llmagent_process(event.to_prompt())
                await message.channel.send(result)
            except Exception as e:
                await message.channel.send(f"Sorry, an error occurred: {type(e).__name__}: {e}")
    # Allow commands to work as well
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
    