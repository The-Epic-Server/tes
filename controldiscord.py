import os
import discord
from discord.ext import commands
print("Starting up pc control")
print("God this is a bad idea")
bot = commands.Bot(command_prefix='>')
bot.remove_command('help')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def help(ctx):
    await ctx.send('''```Commands Help
cmd <command>: run a windows command. Google them. Use & and then another command to run 2 commands. Ex. echo hello & echo hi
set <file> <text>: Resets a file and replaces it with the typed text. Use &n for a new line.
edit <file> <text>: Adds the typed text to the end of a file. Use &n for a new line.
print <file>: Shows the text inside a file.
back <file> <amount>: Removes characters from the end of a file.
mkfile <location> <name>: Creates a file at the location selected. The default location is C:\\Users\\me
mkdir <location> <name>: Creates a folder at the location selected. The default location is C:\\Users\\me```''')

@bot.command()
async def cmd(ctx, *, command):
    os.system(f'cmd /c "cd C:\\Users\\rhone & {command}"')
    await ctx.send(f"Running command: {command}")

@bot.command()
async def set(ctx, file, *, text):
    text = text.replace("&n", '''
''')
    f = open(file, "w")
    f.write(text)
    f.close()
    await ctx.send(f"set {file} to {text}")

@bot.command()
async def edit(ctx, file, *, text):
    text = text.replace("&n", '''
''')
    f = open(file, "a")
    f.write(text)
    f.close()
    await ctx.send(f"Added {text} to {file}")

@bot.command()
async def print(ctx, file):
    f = open(file, "r")
    await ctx.send(f.read())
    f.close()

@bot.command()
async def back(ctx, file, amount=1):
    amount = int(amount)
    f = open(file, "r")
    backspace = f.read()
    f.close
    f = open(file, "w")
    backspace = backspace[:-amount]
    f.write(backspace)
    f.close
    await ctx.send(f"Deleted {amount} characters from the end of {file}")

@bot.command()
async def mkfile(ctx, location, name):
    os.system(f'cmd /c "cd C:\\Users\\rhone\{location} & echo. > {name}"')
    await ctx.send(f"Created file {name} at {location}")

@bot.command()
async def mkdir(ctx, location, name):
    os.system(f'cmd /c "cd C:\\Users\\rhone\{location} & mkdir {name}"')
    await ctx.send(f"Created directory {name} at {location}")

bot.run('NzQwMzc1MzA0NTcyMzcwOTc0.XyoGPA.J4gu8q48j9lq5LMNVGxVAl3XW2s')
