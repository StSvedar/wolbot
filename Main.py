import discord

from Config import *

from Utils.Shell_manager import *
from Utils.Bot import Bot

intents = discord.Intents.all()
bot = Bot(command_prefix = prefix, intents = intents)

# Events
@bot.event # On ready event
async def on_ready():
    bot.log("WOL Bot is ready")
    bot.log("-----------------")

# Commands
@bot.command()  # Test command
async def test(ctx):
    bot.log("Test command")
    await ctx.send("Yeye i'm up and watching you")

@bot.command() # Ping command
async def ping(ctx):
    bot.log("Ping command")
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command() # Wake up command
async def wakeitup(ctx):
    bot.log(f"Wake up command on {mac_address}")
    bot.log(f"Check status of {ipv4}")
    ctx.send("Checking status of the target...")

    if check_status(ipv4):
        bot.log("The target is already up")
        await ctx.send("The target is already up")
        return
    wake_on_lan(mac_address)

    bot.log("Magic packet sent")
    await ctx.send("Waking up the computer")

@bot.command() # Check target status command
async def isup(ctx):
    bot.log(f"Check status command on {ipv4}")
    status = "up" if check_status(ipv4) else "down"
    bot.log(f"{ipv4} is {status}")
    await ctx.send(f"Target is {status}")

@bot.command() # Close command
async def close(ctx):
    bot.log("Close command")
    await ctx.send("Bye bye")
    await bot.close()

bot.run(token)
