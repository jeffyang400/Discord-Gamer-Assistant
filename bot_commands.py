from typing import Final

import discord
from discord.ext import commands
import os
from spotipy import Spotify

from bot_database import list_users, add_user


def command_setup(bot):
    # Command that responds with a simple message
    @bot.command(help="Responds with a greeting message.\nUsage: >hello")
    async def hello(ctx):
        await ctx.send("Hello! I'm a bot. How can I assist you today?")

    # Command that echoes back the user's message
    @bot.command(help="Echoes back the message provided by the user.\nUsage: >echo [message]")
    async def echo(ctx, *, message: str):
        await ctx.send(message)

    @echo.error
    async def echo_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please include a message to echo.")

    # Command that mentions the user
    @bot.command(help="Mentions the user who invoked the command.\nUsage: >mention_me")
    async def mention_me(ctx):
        print(ctx.se)
        await ctx.send(f"Hello {ctx.author.mention}!")

    @bot.command(name="add-gamer", help="Add new gamer to the group. \nUsage: >add-gamer (User ID)")
    async def adduser(ctx, *, user: discord.Member):
        await add_user(user, user.id)
        print(f"{user} has now been added")
        await ctx.send(f"{user.mention} has been added")

    @adduser.error
    async def adduser_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a user to add.")

    @bot.command()
    async def listusers(ctx):
        users = await list_users()
        if users:
            user_list = '\n'.join([f'{user[1]} (ID: {user[0]})' for user in users])
            await ctx.send(f'Users in the database:\n{user_list}')
        else:
            await ctx.send('No users found in the database.')
