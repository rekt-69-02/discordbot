import discord, json, os, asyncio
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    for cogs in os.listdir('./cogs'):
        if cogs.endswith(".py"):
            await bot.load_extension(f'cogs.{cogs[:-3]}')
    # await bot.tree.sync()
    print("I'm ready!!!!")

@bot.command()
async def reload(ctx: commands.Context):
    for cogs in os.listdir('./cogs'):
        if cogs.endswith(".py"):
            await bot.reload_extension(f'cogs.{cogs[:-3]}')
    print('reloaded')
    await ctx.send('reloaded')

with open('token.json', 'r') as jfile:
    a = json.load(jfile)
    bot.run(a['token'])