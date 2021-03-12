import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import get
import asyncio
import random
import time
import os
import requests
import json
import re
def save(savemap, file):
     with open(file, "w") as f:
        json.dump(savemap, f)
def load(file):
    with open(file) as f:
        loadmap = json.load(f)
        return loadmap

class leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def levels(self, ctx):
        toplist = []
        people = load("members.json")
        toplist = [[player, stats["level"]*1000+stats["xp"]] for player, stats in people.items()]
        toplist = sorted(toplist, key=lambda x: x[1], reverse=True)
        top1 = f"<@{toplist[0][0]}> XP: {str(toplist[0][1])}"
        top2 = f"<@{toplist[1][0]}> XP: {str(toplist[1][1])}"
        top3 = f"<@{toplist[2][0]}> XP: {str(toplist[2][1])}"
        top4 = f"<@{toplist[3][0]}> XP: {str(toplist[3][1])}"
        top5 = f"<@{toplist[4][0]}> XP: {str(toplist[4][1])}"
        embed=discord.Embed(title="Leaderboard", description=f'''The top 5 scoring members!
        #1 {top1}
        #2 {top2}
        #3 {top3}
        #4 {top4}
        #5 {top5}''')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def xp(self, ctx, cmd=None, member: discord.Member=None, arg2=None):
        if cmd == None:
            await ctx.send('''Xp Commands:
            xp set <player> <amount> set a players xp
            xp level <player> <amount> set a players level''')
        else:
            people = load("members.json")
            name = str(member.id)
            person = people[name]
            if cmd == "set":
                person["xp"] = int(arg2)
                await ctx.send(f'''Set {member.mention}'s xp to {arg2}''')
                save(people, "members.json")
            if cmd == "level":
                person["level"] = int(arg2)
                await ctx.send(f'''Set {member.mention}'s level to {arg2}''')
                save(people, "members.json")

    @commands.command()
    async def rank(self, ctx, target: discord.Member = None):
        if target == None:
            people = load("members.json")
            person = people[str(ctx.author.id)]
            embed=discord.Embed(title=f"**Rank For {ctx.author}**", description=f'''Level: {person["level"]} Xp: {person["xp"]}/1000''', color=0x00e4f5)
            await ctx.send(embed=embed)
        else:
            people = load("members.json")
            person = people[str(target.id)]
            embed=discord.Embed(title=f"**Rank For {target}**", description=f'''Level: {person["level"]} Xp: {person["xp"]}/1000''', color=0x00e4f5)
            await ctx.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        name = str(message.author.id)
        people = load("members.json")
        if name in people:
            person = people[name]
            person["name"] = message.author.name
            person["tag"] = message.author.discriminator
            earned = random.randint(1, 25)
            person["xp"] = person["xp"]+earned
            if message.content.startswith("!rank"):
                person["xp"] = person["xp"]-earned
            # add a level if they reached levelup xp
            if person["xp"] > 1000:
                person["level"] = person["level"]+1
                person["xp"] = 0
                embed=discord.Embed(title=f"**Level Up!**", description=f'''Congrats {message.author}, you reached level {person["level"]}!''', color=0x00e4f5)
                await message.channel.send(embed=embed)
            save(people, "members.json")
        else:
            people[name] = {"name" : message.author.name, "tag" : message.author.discriminator, "xp" : 1, "level" : 1}
            save(people, "members.json")

def setup(bot):
    bot.add_cog(leveling(bot))