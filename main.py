import discord, json, os, asyncio
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


async def main():
    async with bot:
        for cogs in os.listdir('./cogs'):
            if cogs.endswith(".py"):
                await bot.load_extension(f'cogs.{cogs[:-3]}')
        with open('token.json', 'r') as jfile:
            a = json.load(jfile)
            bot.run(a['token'])    

@bot.event
async def on_ready():
    # await bot.tree.sync()
    print("I'm ready to cum")

@bot.command()
async def sync(ctx: commands.Context):
    s = await bot.tree.sync()
    print(f"synced {s} commands")

@bot.command()
async def reload(ctx: commands.Context):
    for cogs in os.listdir('./cogs'):
        if cogs.endswith(".py"):
            await bot.reload_extension(f'cogs.{cogs[:-3]}')
    print('reloaded')
    await ctx.send('reloaded')

if __name__ == "__main__":
    asyncio.run(main())