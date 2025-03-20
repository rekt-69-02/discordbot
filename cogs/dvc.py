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
        
    @dvc.command()
    async def limit(self, ctx: commands.Context, num=None):
        if ctx.channel.id not in [x["text"] for x in self.settings.values()] or str(ctx.author.id) not in self.user_channels.keys():
            return
        c: discord.VoiceChannel = self.bot.get_channel(self.user_channels[str(ctx.author.id)])
        print(c)
        if num is None:
            await c.edit(user_limit=1)
        else:
            try:
                await c.edit(user_limit=int(num))
            except ValueError:
                await ctx.send("請輸入有效數值")

    @dvc.command()
    async def perm(self, ctx: commands.Context, *members):
        if ctx.channel.id not in [x["text"] for x in self.settings.values()] or str(ctx.author.id) not in self.user_channels.keys():
            return
        c: discord.VoiceChannel = self.bot.get_channel(self.user_channels[str(ctx.author.id)])
        member_list = [ctx.author]
        if members == ():
            await self._set_permission(channel=c, members=member_list)
        else:
            for member in members:
                member_list.append(discord.utils.get(ctx.guild.members, name=member))
            await self._set_permission(channel=c, members=member_list)

    @dvc.command()
    async def name(self, ctx: commands.Context, name:str=None):
        if ctx.channel.id not in [x["text"] for x in self.settings.values()] or str(ctx.author.id) not in self.user_channels.keys():
            return
        c: discord.VoiceChannel = self.bot.get_channel(self.user_channels[str(ctx.author.id)])
        if name == ():
            await c.edit(name=f"{ctx.author.name}的語音頻道")
        else:
            await c.edit(name=name)

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