import discord, json
from discord.ext import commands

class DynamicVoiceChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        with open("dvc.json", "r") as jfile:
            settings = json.load(fp=jfile)
        self.settings: dict = settings
        self.bot = bot
        self.user_channels = {}

    def _update_settings(self):
        with open("dvc.json", "r", encoding="utf8") as jfile:
            settings = json.load(fp=jfile)
            self.settings = settings

    def _get_dvc_category(self, channel: discord.VoiceChannel):
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
        print(self.user_channels)
        # my_id: 891531961405939762
        # ratio_id: 723912925546545183
        if before.channel and after.channel:
            if str(member.id) in self.user_channels.keys():
                if after.channel.id in [x["voice"] for x in self.settings.values()]:
                    await before.channel.delete()
                    self.user_channels.pop(str(member.id))
                    await self._create_and_move(category=before.channel.category, member=member)
                else:
                    await before.channel.delete()
                    self.user_channels.pop()
            for guild in self.settings.values():
                if before.channel.category_id == guild["category"] and after.channel.id == guild["voice"]:
                    category = self._get_dvc_category(after.channel)
                    if category:
                        await self._create_and_move(category=category, member=member)
                    else:
                        pass
                elif after.channel.id == guild["voice"]:
                    pass


        if before.channel is None and after.channel:
            category = self._get_dvc_category(after.channel)
            if category:
                await self._create_and_move(category=category, member=member)
            else:
                pass
        elif before.channel and after.channel is None:
            if str(member.id) in self.user_channels.keys():
                await before.channel.delete()
                self.user_channels.pop(str(member.id))
        """elif before.channel and after.channel:
            category = self._get_dvc_category(after.channel)
            if category:
                await self._create_and_move(category=category, member=member)
            else:
                pass"""

            

async def setup(bot):
    await bot.add_cog(DynamicVoiceChannel(bot=bot))