import discord, json
from discord.ext import commands

class DynamicVoiceChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        with open("dvc.json", "r") as jfile:
            settings = json.load(fp=jfile)
        self.settings: dict = settings
        self.bot: commands.Bot = bot
        self.user_channels = {}

    def _update_settings(self):
        with open("dvc.json", "r", encoding="utf8") as jfile:
            settings = json.load(fp=jfile)
            self.settings = settings

    def _get_dvc_category(self, channel: discord.VoiceChannel):
        if channel is None:
            return None 
        for guild in self.settings.values():
            if guild["voice"] == channel.id:
                category = channel.category
                return category
        return None

    async def _create_and_move(self, category: discord.CategoryChannel, member: discord.Member):
        user_channel = await category.create_voice_channel(name=f"{member.name}的語音頻道")
        await member.move_to(user_channel)
        self.user_channels[f"{member.id}"] = user_channel.id

    @commands.group()
    async def dvc(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Dynamic Voice Channel user manual")
            e.add_field(name="commands", value="`setup`")
            await ctx.send(embed=e)
    
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
        if before.channel and after.channel:
            voice_list = [x["voice"] for x in self.settings.values()]
            if before.channel.id in voice_list:
                pass
            elif str(member.id) in self.user_channels.keys() and after.channel.id in voice_list:
                await before.channel.delete()
                await self._create_and_move(category=after.channel.category, member=member)
            elif str(member.id) in self.user_channels.keys() and after.channel.id not in voice_list:
                await before.channel.delete()
                self.user_channels.pop(str(member.id))
            elif self._get_dvc_category(before.channel) is None and after.channel.id in voice_list:
                category = self._get_dvc_category(after.channel)
                if category:
                    await self._create_and_move(category=category, member=member)
                else:
                    pass
            elif str(member.id) in self.user_channels.keys() and self._get_dvc_category(after.channel.id) is None:
                self.user_channels.pop(str(member.id))
                await before.channel.delete()
        if before.channel is None and after.channel:
            category = self._get_dvc_category(after.channel)
            if category:
                await self._create_and_move(category=category, member=member)
            else:
                pass
        elif before.channel and after.channel is None:
            if str(member.id) in self.user_channels.keys():
                self.user_channels.pop(str(member.id))
                await before.channel.delete()

async def setup(bot):
    await bot.add_cog(DynamicVoiceChannel(bot=bot))