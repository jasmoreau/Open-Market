from commands import *
from util import *

import os
import random
import json
import discord
import sqlite3

from discord.ext import commands, tasks
from dotenv import load_dotenv

conn = sqlite3.connect("./db/userdata.db")
c = conn.cursor()

bot = commands.Bot(command_prefix=".")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Sending greeting message on cmd
@bot.event
async def on_ready():
 print(
     f'{bot.user} is online.'
 )

@bot.event
async def on_guild_join(guild):
    c.execute(f"INSERT INTO server VALUES ({guild.id},'.',1.00)")
    conn.commit()

bot.run(TOKEN)
