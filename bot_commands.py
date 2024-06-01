from typing import Final
from discord.ext import commands
import os
from spotipy import Spotify


def command_setup(bot):
    # Command that responds with a simple message
    @bot.command(help="Responds with a greeting message.\nUsage: >hello")
    async def hello(ctx):
        await ctx.send("Hello! I'm a bot. How can I assist you today?")

    # Command that echoes back the user's message
    @bot.command(help="Echoes back the message provided by the user.\nUsage: >echo [message]")
    async def echo(ctx, *, message: str):
        await ctx.send(message)

    # Command that mentions the user
    @bot.command(help="Mentions the user who invoked the command.\nUsage: >mention_me")
    async def mention_me(ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")