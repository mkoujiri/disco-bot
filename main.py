# bot.py
import csv
import os
from random import *
import requests

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

client = discord.Client(intents=discord.Intents.all())
meg_file='/home/vimguy/disco-bot/megs.csv'
counts_file='/home/vimguy/disco-bot/counts.csv'

quotes_list = []

def load_csv(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        return dict(reader)

def save():
    with open(meg_file, 'w') as csv_file:  
        meg_writer = csv.writer(csv_file)
        for key, value in megs.items():
           meg_writer.writerow([key, value])
    with open(counts_file, 'w') as csv_file:  
        counts_writer = csv.writer(csv_file)
        for key, value in counts.items():
           counts_writer.writerow([key, value])

def read_quotes():
    # read all messages
    API_ENDPOINT = "https://discord.com/api"
    quotes_channel_id = 1159904203242737694
    headers = {
            "authorization": "Bot "+TOKEN
            }
    inputs = {
            "limit":100
            }
    while True:
        data = requests.get(f"{API_ENDPOINT}/channels/{quotes_channel_id}/messages",headers=headers,params=inputs).json()

        for msg in data:
            # process the message
            content = msg['content']
            author = msg['author']['global_name']
            time_stamp = msg['timestamp'][0:10]
            if author is not None:
                if "\"" in content or "-" in content:
                    # message is a quote
                    quotes_list.append(f"This was sent by {author} at {time_stamp}:\n {content}")

        # find oldest message
        inputs["before"]=data[-1]["id"]
        if(len(data) < 100):
            break
    print(f"loaded {len(quotes_list)} quotes")


@bot.command()
async def meg(ctx, user: discord.Member = None):
    if(user):
        if user.nick in megs:
            megs.update({user.nick: str(int(megs.get(user.nick))+1)})
        else:
            megs.update({user.nick: str(1)})

        save()
        await ctx.send(f"megged {user.nick}, they have {megs.get(user.nick)} megs")
    else:
        await ctx.send(f"mention someone that you want to meg fool")
@bot.command()
async def randomapple(ctx):
    file_paths = os.listdir("/home/vimguy/disco-bot/assets/apples")
    file_path = '/home/vimguy/disco-bot/assets/apples/'+file_paths[randint(0,len(file_paths)-1)]
    with open(file_path, 'rb') as f:
        picture = discord.File(f)
        await ctx.send("",file=picture);
@bot.command()
async def randomdisco(ctx):
    file_paths = os.listdir("/home/vimguy/disco-bot/assets/discos")
    file_path = '/home/vimguy/disco-bot/assets/discos/'+file_paths[randint(0,len(file_paths)-1)]
    with open(file_path, 'rb') as f:
        picture = discord.File(f)
        await ctx.send("Aren't they charming?",file=picture);
@bot.command()
async def randomquote(ctx):
    await ctx.send(choice(quotes_list));
@bot.command()
async def reload_quotes(ctx):
    read_quotes()
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
    print(megs.items())
    output = "```"+ "\n".join(f"{key}: {value}" for key,value in sorted(megs.items(),key=lambda item: item[1],reverse=True)) + "```"
    await ctx.send(output)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
# megs = load_csv(meg_file)
# counts = load_csv(counts_file)

read_quotes()
    




bot.run(TOKEN)
