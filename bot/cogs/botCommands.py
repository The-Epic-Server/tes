import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import get
import asyncio
import random
import time
import os
import requests
from lxml import html
import json
import re
def save(savemap, file):
     with open(file, "w") as f:
        json.dump(savemap, f)
def load(file):
    with open(file) as f:
        loadmap = json.load(f)
        return loadmap

class botCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="The Epic Server website")
    async def website(self, ctx):
        embed=discord.Embed(title="The Epic Server Website", url="https://www.theepicserver.tk", description="Join The Epic Server website!", color=0x9b24c6)
        embed.set_thumbnail(url="https://lh6.googleusercontent.com/mFKlaNq8GWQan7JwZe95lYlj6T6BlPVZ3IkYKy8ZAglRW5cYD_KJouuzKQj0ZD6HgzQcvyM=w16383")
        embed.add_field(name="Information, links, minigames, and more!", value="Come check us out at **www.theepicserver.tk**", inline=True)
        await ctx.send(embed=embed)

    @commands.command(brief="shows your latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency*1000, 1)}ms`")

    @commands.command(brief="main command for the tag custom command system")
    async def tag(self, ctx, cmd=None, name=None, *, message=None):
        if cmd == None:
            await ctx.send('''Please enter a sub command!\nSub commands: \n/tag add <name> <message>\n/tag remove <name>\n/tag list''')
        else:
            tags = load("tags.json")
            if cmd == "add":
                if name != None and message != None:
                    if name in tags:
                        await ctx.send("That name already exists! Please pick a new one.")
                        return
                    else:
                        tags[name] = message
                        save(tags, "tags.json")
                        await ctx.send("Added " + name + " to the tags!")
                else:
                    await ctx.send("Please provide a name and message!")
            elif cmd == "remove":
                if name != None:
                    if not name in tags:
                        await ctx.send("That name does not exist! Please enter a new one.")
                        return
                    else:
                        del(tags[name])
                        save(tags, "tags.json")
                        await ctx.send("Removed " + name + " from the tags")
                else:
                    await ctx.send("Please provide a name!")
            elif cmd == "list":
                tags = load("tags.json")
                taglist = ""
                for tag in tags:
                    taglist = taglist + f"{tag}, "
                taglist = taglist[:-2]
                await ctx.send("Here are all of the tags:")
                await ctx.send(f"```{taglist}```")
            else:
                await ctx.send('''Please enter a valid sub command!
            Sub commands: 
            /tag add <name> <message>
            /tag remove <name>''')

    @commands.command(brief="accepts server rules and allows access to the server")
    async def acceptrules(self, ctx, *, code=None):
        if code == None:
            await ctx.message.delete()
            return
        if str(ctx.message.channel.id) == "785582914431221821":
            with open("code.txt") as f:
                if f.read().replace("\n", "") == code:
                    role = get(ctx.author.guild.roles, name="Member")
                    await ctx.author.add_roles(role)
            await ctx.message.delete()
        else:
            await ctx.send("You have already accepted the rules! No need to redo it!")

    @commands.command(brief="claims the prize and gets the @Scavenger role")
    async def prize(self, ctx, *, code=None):
        if code == None:
            await ctx.message.delete()
            return
        if str(ctx.message.channel.id) == "785591834352943185":
            with open("prize.txt") as f:
                if f.read().replace("\n", "") == code:
                    role = get(ctx.author.guild.roles, name="Scavenger")
                    await ctx.author.add_roles(role)
            await ctx.message.delete()
        else:
            await ctx.send("Good for you! You already found the code.")

    @commands.command(brief="the server info stuff")
    async def serverinfo(self, ctx):
        server = ctx.author.guild
        name = server.name
        members = server.member_count
        created = str(server.created_at).split(" ")[0]
        roles = len(server.roles)
        region = str(server.region)
        emojis = len(server.emojis)
        icon = server.icon_url
        owner = str(server.owner)
        embed=discord.Embed(title="Server Info", description="The important server info that nobody wants", color=0x1e00ff)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Created", value=created, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Members", value=members, inline=True)
        embed.add_field(name="Emojis", value=emojis, inline=True)
        await ctx.send(embed=embed)

    @commands.command(brief="dms someone using the bot")
    async def message(self, ctx, member: discord.Member, *, content):
        channel = await member.create_dm()
        await channel.send(content)

    @commands.command(brief="reports a user")
    async def report(self, ctx, member: discord.Member=None, *, reason=None):
        if member == None or reason == None:
            await ctx.send("Please specify a member and a reason!")
            return
        reports = load("reports.json")
        reports.append([ctx.author.mention, member.mention, reason])
        save(reports, "reports.json")
        await ctx.send("Reported " + member.mention + " for " + reason)

    @commands.command(brief="suggest we add your bot to our server")
    async def addbot(self, ctx, id: int=None, reason=None):
        if id == None or reason == None:
            await ctx.send("Please provide your bots id and a reason!")
        elif len(reason.split(" ")) < 100:
            await ctx.send("Your reason isn't descriptive enough! Please make it ~100 words.")
        else:
            await ctx.send("We have sent you request to an admin, and will dm you when we see it.")
            reports = load("bots.json")
            


def setup(bot):
    bot.add_cog(botCommands(bot))