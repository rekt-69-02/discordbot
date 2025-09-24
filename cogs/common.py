from discord.ext import commands
import random, discord, os, asyncio

class MyBotCommon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx: commands.Context, number: int=None):
        try:
            number = int(number)
            if not number:
                await ctx.send(random.randint(0, 100))
            else:
                await ctx.send(random.randint(0, number))
        except ValueError:
            await ctx.send(random.randint(0, 100))

    @commands.command()
    async def avatar(self, ctx: commands.Context, user: discord.Member):
        e = discord.Embed(title=f"{user}'s avatar")
        e.set_image(url=user.avatar.url)
        await ctx.send(embed=e)

    @commands.command()
    async def clean(self, ctx: commands.Context, num: int):
        await ctx.message.delete()
        try:
            history = [message async for message in ctx.channel.history(limit=num)]
            for message in history:
                await message.delete()
        except ValueError:
            await ctx.send("please assign a number!")
    
    @commands.command()
    async def move(self, ctx: commands.Context, num: int, skip: int, channel:discord.TextChannel=None):
        await ctx.message.delete()
        try:
            if not channel:
                channel = await ctx.send("please assign a channel!")
            history = [message async for message in ctx.channel.history(limit=num+skip)]
            history = history[skip:]
            for message in reversed(history):
                if message.attachments:
                    for a in message.attachments:
                        await channel.send(a.url)
                await channel.send(message.content)
                await asyncio.sleep(2)
            for message in history:
                await message.delete()
        except ValueError:
            await ctx.send("please assign a number!")

    @commands.command()
    async def history(self, ctx: commands.Context):
        await ctx.message.delete()
        messages = [message async for message in ctx.channel.history(limit=None)]
        nm = []
        with open(f'temp/{ctx.channel.id}.txt', 'w', encoding='utf8') as file:
            for message in messages:
                nm.append(message.content)
                if message.attachments:
                    for a in message.attachments:
                        nm.append(a.url)
            for new_message in nm:
                file.write(new_message+'\n')
        await ctx.send(file=discord.File(fp=f'temp/{ctx.channel.id}.txt', filename=f'{ctx.channel.id}.txt'))
        os.remove(f'temp/{ctx.channel.id}.txt')

async def setup(bot):
    await bot.add_cog(MyBotCommon(bot=bot))