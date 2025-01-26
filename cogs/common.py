from discord.ext import commands
import random, discord, json

class myBotCommon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx: commands.Context, number=None):
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
        await ctx.send(user.avatar.url)

async def setup(bot):
    await bot.add_cog(myBotCommon(bot))