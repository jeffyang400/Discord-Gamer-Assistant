from typing import Final
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import bot_commands
import bot_spotify
from bot_database import init_db

# Token Entry
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
ID: Final[str] = os.getenv('SPOTIFY_CLIENT_ID')
SECRET: Final[str] = os.getenv('SPOTIFY_CLIENT_SECRET')
URI: Final[str] = os.getenv('SPOTIFY_REDIRECT_URI')


# Bot Intent Setup
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent to read message content
intents.messages = True
intents.guilds = True

# Initialize Bot
bot = commands.Bot(command_prefix=">", intents=intents)
bot_commands.command_setup(bot)
bot_spotify.spotify_setup(bot, ID, SECRET, URI)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - TOKEN ID: {bot.user.id}')
    # Set the bots activity
    activity = discord.Activity(type=discord.ActivityType.listening, name=">help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await init_db()
    print("The Discord Bot is Now Ready!")


def run_bot(token):
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print("Invalid bot token provided. Please check your token and try again.")
    except Exception as e:
        print(f"A token error has occurred: {e}")


if __name__ == '__main__':
    run_bot(TOKEN)
