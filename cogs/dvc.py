import discord, json
from discord import app_commands
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

    async def _set_permission(self, channel: discord.VoiceChannel, members:list[discord.Member]):
        overwrite_user = discord.PermissionOverwrite()
        overwrite_user.connect = True
        overwrite_user.view_channel = True
        overwrite_others = discord.PermissionOverwrite()
        overwrite_others.connect = False
        overwrite_others.view_channel = False
        if len(members) == 0:
            await channel.set_permissions(target=members[0], overwrite=overwrite_user)
            await channel.set_permissions(target=channel.guild.default_role, overwrite=overwrite_others)
        else:
            await channel.set_permissions(target=members[0], overwrite=overwrite_user)
            members.pop(0)
            for member in members:
                await channel.set_permissions(target=member, overwrite=overwrite_user)
            await channel.set_permissions(target=channel.guild.default_role, overwrite=overwrite_others)

    async def _create_and_move(self, category: discord.CategoryChannel, member: discord.Member):
        user_channel = await category.create_voice_channel(name=f"{member.name}的語音頻道")
        await member.move_to(user_channel)
        self.user_channels[f"{member.id}"] = user_channel.id

    DVC = app_commands.Group(name = "dvc", description='Dynamic Voice Channel')
    
    @DVC.command(name="setup", description="Setup a DVC system")
    async def setup(self, interaction: discord.Interaction):
        guild = interaction.guild
        dvc_category = await guild.create_category(name="動態語音頻道")
        dvc_text = await dvc_category.create_text_channel(name="指令")
        dvc_voice = await dvc_category.create_voice_channel(name="點我創建語音頻道")
        with open("dvc.json", "r", encoding="utf8") as jfile:
            j = json.load(fp=jfile)
        with open("dvc.json", "w+", encoding="utf8") as jfile2:
            j[f"{interaction.guild.id}"] = {
                "category": dvc_category.id,
                "text": dvc_text.id,
                "voice": dvc_voice.id
                }
            json.dump(j, jfile2)
        self._update_settings()
        await interaction.response.send_message("Setup complete!", ephemeral=True)

    @DVC.command()
    async def limit(self, interaction: discord.Interaction, num: int=None):
        if interaction.channel.id not in [x["text"] for x in self.settings.values()] or str(interaction.user.id) not in self.user_channels.keys():
            return
        c: discord.VoiceChannel = self.bot.get_channel(self.user_channels[str(interaction.user.id)])
        print(c)
        if num is None:
            await c.edit(user_limit=1)
            await interaction.response.send_message(f"{c.name}的人數上限設為 1", ephemeral=True)
        else:
            try:
                await c.edit(user_limit=int(num))
                await interaction.response.send_message(f"{c.name}的人數上限設為 {num}", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("請輸入有效數值", ephemeral=True)

    @DVC.command()
    async def perm(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.channel.id not in [x["text"] for x in self.settings.values()] or str(interaction.user.id) not in self.user_channels.keys():
            return
        c: discord.VoiceChannel = self.bot.get_channel(self.user_channels[str(interaction.user.id)])
        member_list = member.voice.channel.members
        if not member:
            await self._set_permission(channel=c, members=member_list)
            await interaction.response.send_message(f"頻道權限設為{' '.join([m.name for m in member_list])}", ephemeral=True)
        else:
            await self._set_permission(channel=c, member=member_list)
            await interaction.response.send_message(f"頻道權限設為{' '.join([m.name for m in member_list])}", ephemeral=True)

    @DVC.command()
    async def name(self, interaction: discord.Interaction, name:str=None):
        if interaction.channel.id not in [x["text"] for x in self.settings.values()] or str(interaction.user.id) not in self.user_channels.keys():
            return
        c: discord.VoiceChannel = self.bot.get_channel(self.user_channels[str(interaction.user.id)])
        if name == ():
            await c.edit(name=f"{interaction.user.name}的語音頻道")
            await interaction.response.send_message(f"頻道名稱更改為 {interaction.user.name}的語音頻道", ephemeral=True)
        else:
            await c.edit(name=name)
            await interaction.response.send_message(f"頻道名稱更改為 {name}", ephemeral=True)

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

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.settings.keys():
            voice = self.bot.get_channel(guild["voice"])
            category = voice.category
            for channel in category.channels:
                if channel != voice:
                    await channel.delete()

async def setup(bot):
    await bot.add_cog(DynamicVoiceChannel(bot=bot))