import discord

from Utils.Config_reader import *
from Utils.Shell_manager import *
from Utils.Bot import Bot

try:
    config = Config()
    config.load("config.json")
except FileNotFoundError:
    print("Config file not found : setup.py must be run first")
    exit()

intents = discord.Intents.all()
bot = Bot(command_prefix = config.prefix, intents = intents)

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

@bot.command() # Check target status command
async def isup(ctx):
    bot.log(f"Check status command on {config.ipv4}")
    await ctx.send("Checking target status...")
    status = "up" if check_status(config.ipv4) else "unreachable"
    bot.log(f"{config.ipv4} is {status}")
    await ctx.send(f"Target is {status}")

@bot.command() # Wake up command
async def wakeitup(ctx):
    bot.log(f"Wake up command on {config.mac_address}")
    bot.log(f"Check status of {config.ipv4}")
    await ctx.send("Checking target status...")

    if check_status(config.ipv4):
        bot.log("The target is already up")
        await ctx.send("The target is already up")
        return
    if wake_on_lan(config.mac_address):
        bot.log("Magic packet sent")
        await ctx.send("Waking up the computer")
    else:
        bot.log("Failed to send magic packet")
        await ctx.send("Failed to wake up the computer")

@bot.command() # Shutdown command
async def shutitdown(ctx):
    bot.log(f"Shutdown command on {config.ipv4}")
    bot.log(f"Check status of {config.ipv4}")
    await ctx.send("Checking target status...")

    if not check_status(config.ipv4):
        bot.log("The target is already down")
        await ctx.send("The target is already down")
        return
    if windows_shutdown(config.ipv4, config.user, config.password):
        bot.log("Shutdown command sent")
        await ctx.send("Shutting down the computer")
    else:
        bot.log("Failed to send shutdown command")
        await ctx.send("Failed to shut down the computer")

@bot.command() # Close command
async def close(ctx):
    bot.log("Close command")
    await ctx.send("Bye bye")
    await bot.close()

bot.run(config.token)
