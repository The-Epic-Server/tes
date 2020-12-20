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

class modCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(brief="kicks a member")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Hit by the boot!"):
        embed=discord.Embed(title="Kick!", description=f"Kicked member {member.mention} for reason: {reason}", color=0x00d4fa)
        await ctx.send(embed=embed)
        await member.kick()

    @commands.command(brief="bans a member")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason="The ban hammer has spoken!"):
        embed=discord.Embed(title="Ban!", description=f"Banned member {member.mention} for reason: {reason}", color=0x00d4fa)
        await ctx.send(embed=embed)
        await member.ban()

    @commands.command(brief="mutes a member")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Chat offense"):
        embed=discord.Embed(title="Mute!", description=f"Muted member {member.mention} for reason: {reason}", color=0x00d4fa)
        await ctx.send(embed=embed)
        role = get(member.guild.roles, name="Muted")
        await member.add_roles(role)

    @commands.command(brief="unbans a member")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, id: int, *, reason="Appealed"):
        user = await self.bot.fetch_user(id)
        await discord.Guild.unban(ctx.author.guild, user)
        embed=discord.Embed(title="Unban!", description=f"Unbanned member {user.mention} for reason: {reason}", color=0x00d4fa)
        await ctx.send(embed=embed)

    @commands.command(brief="unmutes a member")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="Mute time up"):
        role = get(member.guild.roles, name="Muted")
        await member.remove_roles(role)
        embed=discord.Embed(title="Unmute!", description=f"Unmuted member {member.mention} for reason: {reason}", color=0x00d4fa)
        await ctx.send(embed=embed)

    @commands.command(brief="changes the name of a member")
    @commands.has_permissions(administrator=True)
    async def cname(self, ctx, person: discord.Member, *, name):
        await person.edit(nick=name)

    @commands.command(brief="deletes a certain amount of messages")
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, amount):
        amount=int(amount)
        amount = amount + 1
        await ctx.channel.purge(limit=amount)

    @commands.command(brief="sets the bots status")
    @commands.has_permissions(administrator=True)
    async def status(self, ctx, *, description=None):
        if description == None:
            game = discord.Game("Being Epic | /help")
            await self.bot.change_presence(activity=game, status=discord.Status.online)
            await ctx.send("Reset my description!")
        else:
            game = discord.Game(description)
            await self.bot.change_presence(activity=game, status=discord.Status.online)
            await ctx.send(f"Changed my description to {description}")

    @commands.command(brief="set the /acceptrules code")
    @commands.has_permissions(administrator=True)
    async def setcode(self, ctx, code="chimkin"):
        with open("code.txt", "w") as f:
            f.write(code)
        await ctx.send("Set the code to " + code)

    @commands.command(brief="sets the /prize code")
    @commands.has_permissions(administrator=True)
    async def setprize(self, ctx, code="chimkin"):
        with open("prize.txt", "w") as f:
            f.write(code)
        await ctx.send("Set the prize code to " + code)

    @commands.command(brief="views a reports by its id number")
    @commands.has_permissions(administrator=True)
    async def viewreports(self, ctx, id=None):
        reports = load("reports.json")
        if id == None:
            await ctx.send("The latest report is number " + str(len(reports)-1))
            return
        try:
            reportnum = int(id)
        except (TypeError, ValueError):
            await ctx.send("Thats not a valid id!")
            return
        try:
            report = reports[reportnum]
        except IndexError:
            await ctx.send("Not a valid report")
            return
        await ctx.send(f'''{report[1]}'s Report\nIssuer: {report[0]}\n{report[2]}''')

def setup(bot):
    bot.add_cog(modCommands(bot))