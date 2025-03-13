import discord
from discord.ext import commands

class DynamicVoiceChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def dvc(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            pass # add manual

    async def _create_voice_channel(guild: discord.Guild, name: str):
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        pass

async def setup(bot):
    await bot.add_cog(DynamicVoiceChannel(bot=bot))