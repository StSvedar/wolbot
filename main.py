import discord

from Config import *

from Utils.Shell_manager import wake_on_lan
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
    wake_on_lan(mac_address)
    bot.log("Magic packet sent")
    await ctx.send("Waking up the computer")

@bot.command() # Close command
async def close(ctx):
    bot.log("Close command")
    await ctx.send("Bye bye")
    await bot.close()

bot.run(token)