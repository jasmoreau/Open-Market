from util import *

import os
import random
import json
import discord
import sqlite3
import finnhub
import ast

from discord.ext import commands, tasks
from dotenv import load_dotenv

from discord.ext.commands import CommandNotFound
load_dotenv()
conn = sqlite3.connect("./db/userdata.db")
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

configuration = finnhub.Configuration(
    api_key={
        'token': os.getenv('FINNHUB_TOKEN')

    }
)
finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))

bot = commands.Bot(command_prefix=".")
TOKEN = os.getenv('DISCORD_TOKEN')

# Sending greeting message on cmd
@bot.event
async def on_ready():
    print(
        f'{bot.user} is online.'
    )


@bot.event
async def on_guild_join(guild):
    c.execute(
        f"INSERT INTO server VALUES ({guild.id},{get_prefix(guild)} = '.',100.00")
    conn.commit()

# @bot.event
# async def on_command_error(ctx, error):
#    if isinstance(error, CommandNotFound):
#        return
#    raise error

load_extensions = ['cmd', 'util']
try:
    for cog in load_extensions:
        bot.load_extension(cog)
except Exception as e:
    print(e)

bot.run(TOKEN)
