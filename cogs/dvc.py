import discord, json
from discord.ext import commands

class DynamicVoiceChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        with open("dvc.json", "r") as jfile:
            settings = json.load(fp=jfile)
        self.settings: dict = settings
        self.bot = bot

    def _update_settings(self):
        with open("dvc.json", "r", encoding="utf8") as jfile:
            settings = json.load(fp=jfile)
            self.settings = settings

    async def _create_voice_channel(guild: discord.Guild, name: str):
        with open(f'dvc/{guild.id}', 'r') as file:
            pass

    @commands.group()
    async def dvc(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            pass # add manual
    
    @dvc.command()
    async def setup(self, ctx: commands.Context):
        guild = ctx.guild
        dvc_category = await guild.create_category(name="動態語音頻道")
        dvc_text = await dvc_category.create_text_channel(name="指令")
        dvc_voice = await dvc_category.create_voice_channel(name="點我創建語音頻道")

        with open("dvc.json", "r", encoding="utf8") as jfile:
            j = json.load(fp=jfile)
        with open("dvc.json", "w", encoding="utf8") as jfile2:
            j[f"{ctx.guild.id}"] = {
                "category": dvc_category.id,
                "text": dvc_text.id,
                "voice": dvc_voice.id
                }
            json.dump(j, jfile2)

        self._update_settings()
            
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        for guild in self.settings.values():
            if after.channel.id == guild["voice"]:
                category = discord.utils.get(after.channel.guild.categories, id=guild["category"])
                user_channel = await category.create_voice_channel(name=f"{member.name}的語音頻道")
                await member.move_to(user_channel)
            

async def setup(bot):
    await bot.add_cog(DynamicVoiceChannel(bot=bot))