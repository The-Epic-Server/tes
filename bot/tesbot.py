import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import random
import time
import os
import requests
from lxml import html
import re
import json

file = open("blocked-words.txt", "r")
content = file.read()
blocked_words = content.split(" ")
file.close()

randomfile = open("random-words.txt", "r")
randomcontent = randomfile.read()
random_words = randomcontent.split(" ")
randomfile.close()

bot = commands.Bot(command_prefix='/')
@bot.event
async def on_ready():
    print('Logged on as The Epic Server#6298')
    game = discord.Game("Being Epic | /help")
    await bot.change_presence(activity=game, status=discord.Status.online)

def save(savemap, file):
    with open(file, "w") as f:
        json.dump(savemap, f)

def load(file):
    with open(file) as f:
        loadmap = json.load(f)
        return loadmap

@bot.command()
async def python(ctx, *, script=None):
    if script != None:
        script = script.replace("```python", "")
        script = script.replace("```py", "")
        script = script.replace("```", "")
        script = script.replace("stdin", "")
        script = script.replace("input(", "")
        script = script.replace("open(", "")
        script = script.replace("import discord", "")
        script = script.replace("import os", "")
        script = script.replace("import subprocess", "")
        with open("script.py", "w") as f:
            f.write(script)
        stream = os.popen('''python3 script.py''')
        output = stream.read()
        if output == "":
            output = "No output."
        embed=discord.Embed(title="Python Script", description='```%s```' % output)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Python Script", description='''Run python in discord!
This is intended to be a simple to use, lightweight python script executor. You can run anything from a simple hello world to advanced computing!
Some features are disabled, such as standard input, exiting, and opening files.
All other python 3.8 features have full functionality. Have fun!
Code Blocks:
Code blocks are a simple and awesome feature that lets you make your code neater!
When running this command (/python <script>) Use **```python** for your code. (make sure to end it with ``` too!)
This will allow you to use new lines without pressing shift enter, will enable pressing tab, and color coding your code!''')
        await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! `{round(bot.latency*1000, 1)}ms`")

@bot.command()
@commands.has_permissions(administrator=True)
async def status(ctx, *, description=None):
    if description == None:
        game = discord.Game("Being Epic | /help")
        await bot.change_presence(activity=game, status=discord.Status.online)
        await ctx.send("Reset my description!")
    else:
        game = discord.Game(description)
        await bot.change_presence(activity=game, status=discord.Status.online)
        await ctx.send(f"Changed my description to {description}")

@bot.command()
async def tag(ctx, cmd=None, name=None, *, message=None):
    if cmd == None:
        await ctx.send('''Please enter a sub command!
        Sub commands: 
        /tag add <name> <message>
        /tag remove <name>
        /tag list''')
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


@bot.command()
async def mcskin(ctx, ign):
    site = requests.get("https://mcuuid.net/?q=%s" % ign)
    sitetext = site.text
    with open("site.html", "w") as f:
        f.write(sitetext)
    root = html.parse("site.html").getroot()
    element = root.get_element_by_id("results_avatar_body")
    r = str(html.tostring(element))
    r = r.replace('''b'<img id="results_avatar_body" class="img-fluid mx-auto" src="''', "")
    r = r.replace('''\\'s Body" loading="lazy">\'''', "")
    r = re.sub(ign, "", r, flags=re.IGNORECASE)
    r = r.replace('''" alt="''', "")
    embed=discord.Embed(title="%s's Skin" % ign, url="https://namemc.com/profile/%s.1" % ign)
    embed.set_thumbnail(url=r)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="Hit by the boot!"):
    embed=discord.Embed(title="Kick!", description=f"Kicked member {member.mention} for reason: {reason}", color=0x00d4fa)
    await ctx.send(embed=embed)
    await member.kick()

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="The ban hammer has spoken!"):
    embed=discord.Embed(title="Ban!", description=f"Banned member {member.mention} for reason: {reason}", color=0x00d4fa)
    await ctx.send(embed=embed)
    await member.ban()

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason="Chat offense"):
    embed=discord.Embed(title="Mute!", description=f"Muted member {member.mention} for reason: {reason}", color=0x00d4fa)
    await ctx.send(embed=embed)
    role = get(member.guild.roles, name="Muted")
    await member.add_roles(role)

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, id: int, *, reason="Appealed"):
    user = await bot.fetch_user(id)
    await discord.Guild.unban(ctx.author.guild, user)
    embed=discord.Embed(title="Unban!", description=f"Unbanned member {user.mention} for reason: {reason}", color=0x00d4fa)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason="Mute time up"):
    role = get(member.guild.roles, name="Muted")
    await member.remove_roles(role)
    embed=discord.Embed(title="Unmute!", description=f"Unmuted member {member.mention} for reason: {reason}", color=0x00d4fa)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def cname(ctx, person: discord.Member, name):
    await person.edit(nick=name)
        
@bot.command()
@commands.has_permissions(administrator=True)
async def delete(ctx, amount):
    amount=int(amount)
    amount = amount + 1
    await ctx.channel.purge(limit=amount)

@bot.command()
async def serverinfo(ctx):
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

@bot.command()
async def rps(ctx, choice):
    choices = ['rock', 'paper', 'scissors']
    botchoice = random.choice(choices)
    if choice == 'rock' and botchoice == 'paper':
        await ctx.send('I chose paper and I win!')
    if choice == 'rock' and botchoice == 'scissors':
        await ctx.send('I chose scissors and you win!')
    if choice == 'rock' and botchoice == 'rock':
        await ctx.send('I chose rock we tied!')
    if choice == 'paper' and botchoice == 'paper':
        await ctx.send('I chose paper and we tied!')
    if choice == 'scissors' and botchoice == 'paper':
        await ctx.send('I chose paper and you win!')
    if choice == 'rock' and botchoice == 'paper':
        await ctx.send('I chose paper and I win!')
    if choice == 'scissors' and botchoice == 'scissors':
        await ctx.send('I chose scissors and we tied!')
    if choice == 'scissors' and botchoice == 'rock':
        await ctx.send('I chose rock and I win!')
    else:
        await ctx.send('Scouts %s' % botchoice)
            
@bot.command()
async def message(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)

@bot.command()
async def text(ctx):
    msg = await ctx.channel.send('the text ')
    await msg.add_reaction('👍') 

@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) == '👍':
        await reaction.message.channel.send('👍')
@bot.event
async def on_message(message):
        if message.author == bot.user:
            return
        if message.content == '/website':
            embed=discord.Embed(title="The Epic Server Website", url="https://www.theepicserver.tk", description="Join The Epic Server website!", color=0x9b24c6)
            embed.set_thumbnail(url="https://lh6.googleusercontent.com/mFKlaNq8GWQan7JwZe95lYlj6T6BlPVZ3IkYKy8ZAglRW5cYD_KJouuzKQj0ZD6HgzQcvyM=w16383")
            embed.add_field(name="Information, links, minigames, and more!", value="Come check us out at **www.theepicserver.tk**", inline=True)
            await message.channel.send(embed=embed)
            
        if any(x in message.content.lower() for x in blocked_words):
            await message.delete()

        if message.content == '/speedtype':
            words = [random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words), random.choice(random_words)]
            words = " ".join(words)
            await message.channel.send("You will have 60 seconds to type the text")
            await message.channel.send("Please don't copy paste")
            await message.channel.send("3")
            time.sleep(1)
            await message.channel.send("2")
            time.sleep(1)
            await message.channel.send("1")
            time.sleep(1)
            await message.channel.send("GO!")
            await message.channel.send("Type this:")
            await message.channel.send(words)
            starttime = time.time()
            msg = await bot.wait_for('message', timeout=60)
            youtyped = msg.content
            await message.channel.send(f'You typed: ```{youtyped}```')
            stoptime = time.time()
            fulltime = stoptime-starttime
            fulltime = round(fulltime)
            await message.channel.send (f"You took: **{fulltime}** seconds!")
        
        if message.content.startswith("/"):
            tags = load("tags.json")
            tag = message.content.replace("/", "")
            if tag in tags:
                await message.channel.send(tags[tag])

        await bot.process_commands(message)
with open("token.txt") as f:
    bot.run(f.read())
