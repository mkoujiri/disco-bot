# bot.py
import csv
import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

client = discord.Client(intents=discord.Intents.all())

def load_csv():
    with open('megs.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        return dict(reader)

def save_to_csv():
    with open('megs.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in megs.items():
           writer.writerow([key, value])

@bot.command()
async def meg(ctx, user: discord.Member = None):
    if(user):
        if str(user) in megs:
            megs.update({str(user): int(megs.get(str(user)))+1})
        else:
            megs.update({str(user): 1})

        save_to_csv()
        await ctx.send(f"megged {user}, they have {megs.get(str(user))} megs")
    else:
        await ctx.send(f"mention someone that you want to meg fool")

@bot.command()
async def megboard(ctx):
    output = "```"+ "\n".join(f"{key}: {value}" for key,value in megs.items()) + "```"
    await ctx.send(output)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

megs = load_csv()
bot.run(TOKEN)
