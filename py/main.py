from commands import *
from util import *

import os
import random
import json
import discord
import sqlite3

from discord.ext import commands, tasks
from dotenv import load_dotenv

from discord.ext.commands import CommandNotFound
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
    c.execute(f"INSERT INTO server VALUES ({guild.id},{get_prefix(guild)} = '.',100.00")
    conn.commit()



@bot.command(aliases=['setdaily'])
async def set_daily_reward(ctx, *, amount: float):
    daily_reward = format(amount, '.2f')
    c.execute(f"UPDATE server SET daily = {daily_reward} WHERE id = {ctx.guild.id}")
    conn.commit()
    await ctx.send(f"Set daily reward to  ${daily_reward}");


#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, CommandNotFound):
#        return
#    raise error

bot.run(TOKEN)
