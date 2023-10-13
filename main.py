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
meg_file='/home/vimguy/disco-bot/megs.csv'
counts_file='/home/vimguy/disco-bot/counts.csv'

def load_csv(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        return dict(reader)

def save(csv_file):
    with open(csv_file, 'w') as csv_file:  
        meg_writer = csv.writer(csv_file)
        for key, value in megs.items():
           writer.writerow([key, value])
    with open(csv_file, 'w') as csv_file:  
        counts_writer = csv.writer(counts_file)
        for key, value in counts.items():
           writer.writerow([key, value])

@bot.command()
async def meg(ctx, user: discord.Member = None):
    if(user):
        if str(user) in megs:
            megs.update({str(user): int(megs.get(str(user)))+1})
        else:
            megs.update({str(user): 1})

        save()
        await ctx.send(f"megged {user}, they have {megs.get(str(user))} megs")
    else:
        await ctx.send(f"mention someone that you want to meg fool")

@bot.command()
async def apple(ctx):
    if 'apple' in counts:
        counts.update({'apple': int(counts.get('apple'))+1})
    else:
        counts.update({'apple': 1})
    save()
    await ctx.send(f"APPLE!!! {counts.get('apple')} apples")

@bot.command()
async def bread(ctx):
    if 'bread' in counts:
        counts.update({'bread': int(counts.get('bread'))+1})
    else:
        counts.update({'bread': 1})
    save()
    await ctx.send(f"Get that bread!!! {counts.get('bread')} breadsticks")

@bot.command()
async def pizza(ctx):
    if 'pizza' in counts:
        counts.update({'pizza': int(counts.get('pizza'))+1})
    else:
        counts.update({'pizza': 1})
    save()
    await ctx.send(f"Get that pizza, go for the thin slices!!! {counts.get('pizza')} pizza slices")

@bot.command()
async def megboard(ctx):
    output = "```"+ "\n".join(f"{key}: {value}" for key,value in megs.items()) + "```"
    await ctx.send(output)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
megs = load_csv(meg_file)
counts = load_csv(counts_file)
bot.run(TOKEN)
