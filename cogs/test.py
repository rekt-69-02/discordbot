import discord, json
from discord.ext import commands

class MyBotTest(commands.Cog):
    def __init__(self, bot):
        with open("dvc.json", "r") as jfile:
            f = json.load(jfile)
            self.settings: dict = f
        self.bot = bot


    @commands.command()
    async def get_category(self, ctx: commands.Context, id):
        category = discord.utils.get(ctx.guild.categories, id=int(id))
        if category is None:
            await ctx.send("u suck")
        else:
            await ctx.send(category)

    @commands.command()
    async def print_item(self, ctx):
        await ctx.send(self.settings)
        for i in self.settings.items():
            print(i)

    @commands.command()
    async def clean_dvc(self, ctx: commands.Context):
        for c in ctx.guild.categories:
            if c.name == "動態語音頻道":
                for ch in c.channels:
                    await ch.delete()
                await c.delete()

    @commands.command()
    async def get_user(self, ctx: commands.Context, member=None):
        user = discord.utils.get(ctx.guild.members, name=member)
        print(user)
        
async def setup(bot):
    await bot.add_cog(MyBotTest(bot=bot))
        