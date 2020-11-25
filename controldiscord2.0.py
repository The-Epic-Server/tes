import discord
from discord.ext import commands
from pyautogui import screenshot
import keyboard
import pyautogui
import mouse as m
import asyncio
import os
tokenf = open("token.txt")
token = tokenf.read()
tokenf.close()

prefixf = open("prefix.txt")
prefix = prefixf.read()
prefixf.close()

bot = commands.Bot(command_prefix=prefix)

@bot.command()
async def ss(ctx):
    await ctx.send("Took screenshot, attempting to send it")
    shot = screenshot()
    shot.save("ss.png")
    with open(f'ss.png', 'rb') as f:
        await ctx.send(file=discord.File(f, 'screenshot.png'))

@bot.command()
async def mousetp(ctx, x=None, y=None):
    if x == None or y == None:
        await ctx.send("The current mouse coords are: " + str(m.get_position()))
    elif y == None:
        await ctx.send("The current mouse coords are: " + str(m.get_position()))
    else:
        x = int(x)
        y = int(y)
        m.move(x, y)
        await ctx.send("Moved mouse to " + str(x) + " " + str(y))

@bot.command()
async def mouse(ctx, x=0, y=0):
    await ctx.send("Moving mouse...")
    m.move(x, y, False, 1)
    await ctx.send("Moved mouse successfully")

@bot.command()
async def key(ctx, key, time=1):
    await ctx.send("Pressing " + key + " for " + str(time) + " seconds")
    for x in range(0, time):
        keyboard.press(key)
        await asyncio.sleep(1)
        keyboard.release(key)
    await ctx.send("Finished pressing " + key)

@bot.command()
async def type(ctx, *, string):
    for letter in string:
        if len(letter) > 1:
            letter = letter.lower()
        if letter == "\n":
            keyboard.press_and_release("shift+enter")
        else:
            pyautogui.press(letter, _pause=False)
        await asyncio.sleep(0.25)
    keyboard.press("enter")
    await ctx.send("Typed " + string)

@bot.command()
async def lclick(ctx, amount=1):
    await ctx.send("Started left clicking " + str(amount) + " times")
    for x in range(0, amount):
        m.click()
        await asyncio.sleep(0.1)
    await ctx.send("Finished left clicking")

@bot.command()
async def rclick(ctx, amount=1):
    await ctx.send("Started right clicking " + str(amount) + " times")
    for x in range(0, amount):
        m.click("right")
        await asyncio.sleep(0.1)
    await ctx.send("Finished right clicking")

@bot.command()
async def holdlclick(ctx, time):
    await ctx.send("Started holding left click for " + str(time) + " seconds")
    m.hold()
    time = int(time)
    await asyncio.sleep(time)
    m.release()
    await ctx.send("Finished holding left click")

@bot.command()
async def holdrclick(ctx, time):
    await ctx.send("Started holding left click for " + str(time) + " seconds")
    m.hold("right")
    time = int(time)
    await asyncio.sleep(time)
    m.release("right")
    await ctx.send("Finished holding right click")

@bot.command()
async def bounds(ctx):
    coords = m.get_position()
    m.move(1000000, 1000000)
    await ctx.send("The screen boundries are: 0,0 x " + str(m.get_position()[0]) + "," + str(m.get_position()[1]))
    m.move(coords[0], coords[1])

@bot.command()
async def shutdown(ctx):
    await ctx.send("This will completly shut down the bot.")
    await ctx.send("If you made a big error use /accident to restart the bot")
    await ctx.send("Type YES to shut down")
    def check(author):
        def inner_check(message): 
            if message.author != author:
                return False
            else:
                if message.channel == ctx.channel:
                    return True
                else:
                    return False

        return inner_check

    option = await bot.wait_for("message", check=check(ctx.author))
    if option.content.upper() == "YES":
        await ctx.send("Shutting bot down...")
        exit()
    else:
        await ctx.send("Cancelling...")

@bot.command()
async def accident(ctx):
    await ctx.send("Bot will restart in 5 seconds.")
    await asyncio.sleep(5)
    await ctx.send("Reloading bot...")
    os.system("start py controldiscord2.0.py")
    exit()

bot.run(token)
