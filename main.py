from typing import Final
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask, request, redirect
import bot_commands
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

import threading

# Token Entry
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
ID: Final[str] = os.getenv('SPOTIFY_CLIENT_ID')
SECRET: Final[str] = os.getenv('SPOTIFY_CLIENT_SECRET')
URI: Final[str] = os.getenv('SPOTIFY_REDIRECT_URI')

sp_oauth = SpotifyOAuth(
    client_id=ID,
    client_secret=SECRET,
    redirect_uri=URI,
    scope='user-library-read'
)

app = Flask(__name__)


@app.route('/callback')
def spotify_callback():
    code = request.args.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code)
        if token_info:
            return "Spotify authentication is complete. You can close this window."
        else:
            return "Failed to get the access token."
    return "No code provided."


def run_flask():
    app.run(host='0.0.0.0', port=8888)


# Running Flask in a separate thread
threading.Thread(target=run_flask).start()

# Bot Intent Setup
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent to read message content
intents.messages = True
intents.guilds = True

# Initialize Bot
bot = commands.Bot(command_prefix=">", intents=intents)
bot_commands.setup(bot)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - TOKEN ID: {bot.user.id}')
    # Set the bot's activity
    activity = discord.Activity(type=discord.ActivityType.listening, name=">help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("The Discord Bot is Now Ready!")


@bot.command(name='spotify')
async def fetch_spotify(ctx, *, query):
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        await ctx.send(f'Please authenticate with Spotify by clicking [here]({auth_url})')
        return

    sp = Spotify(auth=token_info['access_token'])
    results = sp.search(q=query, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        title = track['name']
        artist = track['artists'][0]['name']
        url = track['external_urls']['spotify']
        response = f"**{title}** by **{artist}**\nListen here: {url}"
    else:
        response = "No results found for your query."

    await ctx.send(response)


def run_bot(token):
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print("Invalid bot token provided. Please check your token and try again.")
    except Exception as e:
        print(f"A token error has occurred: {e}")


if __name__ == '__main__':
    run_bot(TOKEN)