import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import random
import time
my_file = open("blocked-words.txt", "r")
content = my_file.read()
blocked_words = content.split(" ")
my_file.close()

bot = commands.Bot(command_prefix='/')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged on as The Epic Server#6298')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def help(ctx, command=None):
    if command == None:
        await ctx.send('''**The Epic Server Help Menu**
**Prefix**
```To execute any command on the epic server, you the prefix / followed by a command. Different bots have different prefixes.```
**Arguments**
```Many command have arguments, or extra text added after to change the outcome. An argument is shown with <argument>. If an argument has + at the end, it means it can be multi word.```
**Commands**
```help <command> Show this list

ping Nothing special. Just to ping the bot and check if it responds.

mention <person> <times> A little prank. Can be used to spam someone. Times caps out at 10.

cname <person> <name+> Change someone name. Can only be used by admins.

delete <amount> Deletes a certain amount of messages. Can only be used my admins.

rps <rock/paper/scissors> Play a game of rock, paper, scissors with the bot!

message <person> <message+> Send a dm to someone using the bot!

website Shows a fancy message displaying the website link!```''')
    elif command == "ping":
        await ctx.send("```ping Nothing special. Just to ping the bot and check if it responds.```")
    elif command == "mention":
        await ctx.send("```mention <person> <times> A little prank. Can be used to spam someone. Times caps out at 10.```")
    elif command == "cname":
        await ctx.send("```cname <person> <name+> Change someone name. Can only be used by admins.```")
    elif command == "rps":
        await ctx.send("```rps <rock/paper/scissors> Play a game of rock, paper, scissors with the bot!```")
    elif command == "website":
        await ctx.send("```website Shows a fancy message displaying the website link!```")
    elif command == "delete":
        await ctx.send("```delete <amount> Deletes a certain amount of messages. Can only be used my admins.```")
    else:
        await ctx.send(f"```{command} unknown command. Type /help for help.```")

@bot.command()
async def mention(ctx, person, times):
    times = int(times)
    times = times - 1
    for x in range(0, times):  
        await ctx.send(f'hey {person}')

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
async def timer(ctx, time):
    if time > 10:
        int(time)
        time = time + 1
        for x in range(1, time):
            time.sleep(1)
            ctx.send(x)
            
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
        if message.content == '/website':
            embed=discord.Embed(title="The Epic Server Website", url="https://www.theepicserver.tk", description="Join The Epic Server website!", color=0x9b24c6)
            embed.set_thumbnail(url="https://lh6.googleusercontent.com/mFKlaNq8GWQan7JwZe95lYlj6T6BlPVZ3IkYKy8ZAglRW5cYD_KJouuzKQj0ZD6HgzQcvyM=w16383")
            embed.add_field(name="Information, links, minigames, and more!", value="Come check us out at **www.theepicserver.tk**", inline=True)
            await message.channel.send(embed=embed)
            
        if any(x in message.content.lower() for x in blocked_words):
            await message.delete()
        await bot.process_commands(message)
bot.run('')
