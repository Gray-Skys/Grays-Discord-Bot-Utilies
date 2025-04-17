import discord
from discord.ext import commands
import asyncio
import random
import re

# === Configuration ===
BOT_TOKEN = "ABC123FIXME"  # Replace this with your bot's token
CHANNEL_ID = ABC123FIXME  # Replace with your actual channel ID

# === Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await asyncio.sleep(1)

    channel = bot.get_channel(CHANNEL_ID)
    if channel and isinstance(channel, discord.TextChannel):
        try:
            await channel.send("Dice man on")
            print(f"Startup message sent to #{channel.name}")
        except Exception as e:
            print(f"Failed to send message: {e}")
    else:
        print("Could not find the channel or it is not a text channel.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Matches: !d20, !D20, !d 20, !D 20 (case insensitive)
    match = re.match(r"!d\s*(\d+)", message.content.strip(), re.IGNORECASE)
    if match:
        sides = int(match.group(1))
        if sides < 1:
            await message.channel.send("Dice must have at least 1 side.")
        else:
            result = random.randint(1, sides)
            await message.channel.send(f"You rolled a {result} on a D{sides}!")

    await bot.process_commands(message)

# === Start the Bot ===
if __name__ == "__main__":
    print("Starting Dice Bot...")
    bot.run(BOT_TOKEN)