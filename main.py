import discord
from discord.ext import commands
from config import *
from wol import wake_on_lan

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = prefix, intents = intents) 

@bot.event
async def on_ready():
    print("WOL Bot is ready")
    print("-----------------")


@bot.command()
async def test(ctx):
    await ctx.send("Yeye i'm up and watching you")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def wakeitup(ctx):
    wake_on_lan(mac_address)
    await ctx.send("Waking up the computer")

bot.run(token)