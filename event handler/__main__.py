import discord
from discord.ext import commands
from discord.ext import tasks
import time
import database

bot = commands.Bot(command_prefix=">")


@tasks.loop(seconds=1)
async def test():
    print("hi")

@tasks.loop(seconds=1)
async def maintask():
    t = time.asctime()
    t = t.split(" ")
    events = database.load("events.json")
    for event in events:
        if events[event] == None:
            return
        if events[event]["month"] == t[1]:
            if events[event]["day"] == t[2]:
                if events[event]["time"] == t[3][:-3]:
                    print(str(event) + " is starting!")
                    channel = bot.get_channel(713381467463614565)
                    await channel.send("The event " + event + " is starting now!")
                    events[event] = None
                    database.save(events, "events.json")
                else:
                    print(events[event]["time"])
                    print(t[3][:-3])
                    print("wrong time")
                    return
            else:
                print(events[event]["day"])
                print("wrong dat")
                return
        else:
            print(events[event]["month"])
            print("wrong moneth")
            return
@bot.event
async def on_ready():
    print("ready")
    events = database.load("events.json")
    print(events)
    maintask.start()
with open("token.txt") as f: 
    bot.run(f.read())
