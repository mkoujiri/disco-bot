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
            megs.update({str(user): str(int(megs.get(str(user)))+1)})
        else:
            megs.update({str(user): str(1)})

        save()
        await ctx.send(f"megged {user}, they have {megs.get(str(user))} megs")
    else:
        with open("test_image.png", 'rb') as f:
            picture = discord.file(f)
            await ctx.send(f"mention someone that you want to meg fool", file=picture)

@bot.command()
async def apple(ctx, count: int = 1):
    if 'apple' in counts:
        counts.update({'apple': str(int(counts.get('apple'))+count)})
    else:
        counts.update({'apple': str(count)})
    save()
    await ctx.send(f"APPLE!!! {counts.get('apple')} apples")

@bot.command()
async def bread(ctx, count: int = 1):
    if 'bread' in counts:
        counts.update({'bread': str(int(counts.get('bread'))+count)})
    else:
        counts.update({'bread': str(count)})
    save()
    await ctx.send(f"Get that bread!!! {counts.get('bread')} breadsticks")

@bot.command()
async def pizza(ctx, count: int = 1):
    if 'pizza' in counts:
        counts.update({'pizza': str(int(counts.get('pizza'))+count)})
    else:
        counts.update({'pizza': str(count)})
    save()
    await ctx.send(f"Get that pizza, go for the thin slices!!! {counts.get('pizza')} pizza slices")

@bot.command()
async def reset(ctx):
    counts.update({'pizza': str(0)})
    counts.update({'bread': str(0)})
    save()
    await ctx.send(f"Reset pizza and bread counters");

@bot.command()
async def megboard(ctx):
    output = "```"+ "\n".join(f"{key}: {value}" for key,value in sorted(megs.items())) + "```"
    await ctx.send(output)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
megs = load_csv(meg_file)
counts = load_csv(counts_file)
bot.run(TOKEN)
