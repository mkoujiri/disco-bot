# bot.py
import csv
import os
from random import *
import requests
import time
import jsonpickle

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APP_ID = "1142918946492784731"
DISCO_SERVER_ID = '1011844778813558874'

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

LOCAL = True
if not LOCAL:
    meg_file='/home/vimguy/disco-bot/megs.csv'
    counts_file='/home/vimguy/disco-bot/counts.csv'
    apple_dir="/home/vimguy/disco-bot/assets/apples"
    disco_dir="/home/vimguy/disco-bot/assets/discos"
    summer_comp_dir='/home/vimguy/disco-bot/assets/summer'
    summer_comp_file='/home/vimguy/disco-bot/assets/summer/log.csv'
else:
    meg_file='/home/mkoujiri/programming/disco_bot/megs.csv'
    counts_file='/home/mkoujiri/programming/disco_bot/counts.csv'
    apple_dir="/home/mkoujiri/programming/disco_bot/assets/apples"
    disco_dir="/home/mkoujiri/programming/disco_bot/assets/discos"
    summer_comp_dir='/home/mkoujiri/programming/disco_bot/assets/summer'
    summer_comp_file='/home/mkoujiri/programming/disco_bot/assets/summer/log.csv'

quotes_list = []


def load_csv(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        return dict(reader)

class Activity:
    def __init__(self,activity_type,points,description):
        self.type = activity_type
        self.points = points
        self.description = description
        self.time_stamp = time.time()

class UserLog:
    def __init__(self):
        self.activities = []
    def add_activity(self,activity_type,points,description):
        self.activities.append(Activity(activity_type,points,description))
    def total_points(self):
        return sum([x.points for x in self.activities])
    def display_activities(self):
        output = "```\n"+"\n".join([f"{time.strftime('%Y-%m-%d', time.localtime(activity.time_stamp))}: {activity.type}, {activity.description}" for activity in sorted(self.activities,key=lambda activity: activity.time_stamp)])+"\n```"
        return output



def save():
    with open(meg_file, 'w') as csv_file:  
        meg_writer = csv.writer(csv_file)
        for key, value in megs.items():
           meg_writer.writerow([key, value])
    with open(counts_file, 'w') as csv_file:  
        counts_writer = csv.writer(csv_file)
        for key, value in counts.items():
           counts_writer.writerow([key, value])
    with open(summer_comp_file, 'w') as f:
        try:
            f.write(jsonpickle.encode(summer_logs))
        except Exception as e:
            print(e)


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

        if(not isinstance(data,list)):
            time.sleep(1)
            continue
        for msg in data:
            # process the message
            try:
                content = msg['content']
                author = msg['author']['global_name']
                time_stamp = msg['timestamp'][0:10]
                if author is not None:
                    if "\"" in content or "-" in content:
                        # message is a quote
                        quotes_list.append(f"This was sent by {author} at {time_stamp}:\n {content}")
            except Exception as e:
                print(e)
                print("failed to load quotes")
                return
        time.sleep(.5)

        # find oldest message
        inputs["before"]=data[-1]["id"]
        if(len(data) < 100):
            break
    print(f"loaded {len(quotes_list)} quotes")


def save_attachments(ctx,directory):
    try:
        for attachment in ctx.message.attachments:
            # image saved
            ftype = attachment.url.split('/')[-1]
            myfile = requests.get(attachment.url)
            open(f'{directory}/{attachment.filename}', 'wb').write(myfile.content)
    except AttributeError as e:
        return

@bot.command()
async def adddisco(ctx):
    save_attachments(ctx,disco_dir)

@bot.command()
async def addapple(ctx):
    save_attachments(ctx,apple_dir)

@bot.slash_command(name="summer",description="slash command")
async def summer(ctx,activity_type: discord.Option(str,choices=["sprints","throws","film","lift","misc"]),points: discord.Option(int),description: discord.Option(str)):
    save_attachments(ctx,summer_comp_dir)

    user_id = f"{ctx.author.id}"
    if user_id not in summer_logs:
        summer_logs[user_id] = UserLog()
    summer_logs[user_id].add_activity(activity_type,points,description)
    save()
    await ctx.respond(f"Added {activity_type}: {description}, you now have: {summer_logs[user_id].total_points()} points")

@bot.command()
async def summerlog(ctx, user: discord.Member = None):
    user_id = f"{ctx.author.id}"
    if(user):
        user_id = f"{user.id}"
    try:
        await ctx.send(summer_logs[user_id].display_activities())
    except KeyError as e:
        pass

@bot.command()
async def summerboard(ctx):
    output = "```\n"
    for key,value in sorted(summer_logs.items(),key=lambda item: item[1].total_points(), reverse=True):
        guild = await bot.fetch_guild(DISCO_SERVER_ID)
        user = await guild.fetch_member(key)
        if user.nick is not None:
            output+=f"{user.nick},{value.total_points()}\n"
        else:
            output+=f"{user.display_name},{value.total_points()}\n"
    output+='```'
    await ctx.send(output)

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
    await ctx.send("Updated quotes");
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
    output = "```"+ "\n".join(f"{key}: {value}" for key,value in sorted(megs.items(),key=lambda item: item[1],reverse=True)) + "```"
    await ctx.send(output)

megs = load_csv(meg_file)
counts = load_csv(counts_file)
summer_logs = {}
with open(summer_comp_file,"r") as f:
    summer_logs = jsonpickle.decode(f.read())



read_quotes()

bot.run(TOKEN)
