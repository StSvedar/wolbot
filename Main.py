import discord

from Utils.Config_reader import *
from Utils.Shell_manager import *
from Utils.Bot import Bot

# Utils
def wrong_config_exit():
    print(f"Go to {CONFIG_FILE} to fix the configuration")
    exit()

async def command_target(ctx, target_name:str = None):
    target = None

    if target_name:
        target = config.get_target_by_name(target_name)
        if target is None:
            bot.log(f"Target not found : {target_name}")
            await ctx.send(f"Target not found : {target_name}")
            return None
    else:
        target = config.default_target
        if target is None:
            bot.log("No default target")
            await ctx.send("No default target")
            return None
        
    return target

# Main
config = Config()
try:
    config.load(CONFIG_FILE)
except FileNotFoundError:
    print("Config file not found, creating a new one")
    config.prefix = input("Enter the command prefix : ")
    config.token = input("Enter the bot token : ")
    config.save(CONFIG_FILE)
except ValueError as e:
    print(e)
    wrong_config_exit()

if not config.is_complete():
    print("Config file is not complete")
    wrong_config_exit()

try:
    intents = discord.Intents.all()
    bot = Bot(command_prefix = config.prefix, intents = intents)
except discord.LoginFailure as e:
    print(e)
    wrong_config_exit()

# Events
@bot.event # On ready event
async def on_ready():
    if config.default_target is not None:
        print(f"mac : {config.default_target.mac_address}, ipv4 : {config.default_target.ipv4}")
    bot.log("WOL Bot is ready")
    bot.log("-----------------")

# Commands
@bot.command() # Ping command
async def ping(ctx):
    bot.log("Ping command")
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command() # List targets command
async def list(ctx):
    bot.log("List command")
    if len(config.targets) == 0:
        bot.log("No target")
        await ctx.send("No target")
        return

    message = "Targets :\n"
    for target in config.targets:
        message += f"- {target.name} : {target.os} {target.user} {target.mac_address} {target.ipv4}"
        if target == config.default_target:
            message += " (default)"
        message += "\n"
    bot.log(message)
    await ctx.send(message)

@bot.command() # Add target command
async def add(ctx, name=None, os=None, user=None, password=None, mac=None, ipv4=None):
    bot.log("Add command")
    
    if not all([name, os, user, password, mac]):
        bot.log("Missing arguments")
        await ctx.send("Missing arguments : correct format : add <name> <os> <user> <password> <mac> [ipv4]")
        return
    
    bot.log(f"Name : {name}, OS : {os}, User : {user}, Password : {password}, MAC : {mac}, IPv4 : {ipv4}")

    if ipv4 is None:
        ipv4 = "AUTO"

    try:
        config.add_target(Target(name, user, os, password, mac, ipv4))
        config.save(CONFIG_FILE)
    except Exception as e:
        bot.log(e)
        await ctx.send(e)
        return
    
    bot.log(f"Target added : {name}")
    await ctx.send(f"Target added : {name}")

@bot.command() # Set default target command
async def setdefault(ctx, name):
    bot.log("Set default command")
    try:
        config.set_default_target(name)
        config.save(CONFIG_FILE)
        bot.log(f"Default target set : {name}")
        await ctx.send(f"Default target set : {name}")
    except ValueError as e:
        bot.log(e)
        await ctx.send(e)

@bot.command() # Remove target command
async def remove(ctx, name):
    bot.log("Remove command")
    target = config.get_target_by_name(name)
    if target is None:
        bot.log(f"Target not found : {name}")
        await ctx.send(f"Target not found : {name}")
        return

    config.remove_target(target)
    config.save(CONFIG_FILE)
    bot.log(f"Target removed : {name}")
    await ctx.send(f"Target removed : {name}")

@bot.command() # Check target status command
async def isup(ctx, target_name=None):
    bot.log(f"Check status command")
    target = await command_target(ctx, target_name)
    if target is None:
        return

    if target.ipv4 is None:
        bot.log("No target ip address")
        await ctx.send("No target ip address")
        return

    await ctx.send("Checking target status...")
    
    status = "up" if check_status(target.ipv4) else "unreachable"
    
    bot.log(f"{target.ipv4} is {status}")
    await ctx.send(f"Target is {status}")

@bot.command() # Wake up command
async def wakeup(ctx, target_name=None):
    bot.log(f"Wake up command")
    target = await command_target(ctx, target_name)
    if target is None:
        return
    
    bot.log(f"Check status")
    if target.ipv4 is None:
        bot.log("No target ip address")
        await ctx.send("No target ip address")
        return
    if target.mac_address is None:
        bot.log("No target mac address")
        await ctx.send("No target mac address")
        return

    await ctx.send("Checking target status...")

    if check_status(target.ipv4):
        bot.log("The target is already up")
        await ctx.send("The target is already up")
        return
    
    if wake_on_lan(target.mac_address):
        bot.log("Magic packet sent")
        await ctx.send(f"Waking up {target.name}")
    else:
        bot.log("Failed to send magic packet")
        await ctx.send("Failed to wake up the computer")

@bot.command() # Shutdown command
async def shutdown(ctx, target_name=None):
    bot.log(f"Shutdown command")
    target = await command_target(ctx, target_name)
    if target is None:
        return

    bot.log(f"Check status")
    if target.ipv4 is None:
        bot.log("No target ip address")
        await ctx.send("No target ip address")
        return
    if target.user is None:
        bot.log("No target user")
        await ctx.send("No target user")
        return

    await ctx.send("Checking target status...")

    if not check_status(target.ipv4):
        bot.log("The target is already down")
        await ctx.send("The target is already down")
        return
    
    success = False
    if target.os is 'linux':
        success = linux_shutdown(target.ipv4, target.user)
    elif target.os is 'windows':
        success = windows_shutdown(target.ipv4, target.user, target.password)

    if success:
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
