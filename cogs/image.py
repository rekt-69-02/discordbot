import discord
from PIL import Image, ImageSequence
from discord.ext import commands

class my_bot_Image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def cum(self, ctx, user):

        def _resize_image(image):
            i = Image.open(image)
            i = i.resize((256, 256), Image.Resampling.LANCZOS)
            i.save(image)

        def _cum(uid):
            bg_path = f'folder/img_temp/{uid}.png'
            bg = Image.open(bg_path)
            if bg.size != (256, 256):
                _resize_image(bg_path)  
            overlay = Image.open('folder/img_resource/cum1.png')
            bg = Image.open(bg_path)
            bg.paste(overlay, (0, 0), mask = overlay)
            bg.save(f'folder/img_temp/{uid}.png')

        u: discord.User = discord.utils.find(lambda m: m.name == user, ctx.guild.members)
        if u is None:
            u = ctx.author
        
        # if u.avatar.is_animated():
        await u.avatar.save(f"folder/img_temp/{u.id}.png")
        _cum(u.id)
        await ctx.send(file=discord.File(f"folder/img_temp/{u.id}.png"))

async def setup(bot):
    await bot.add_cog(my_bot_Image(bot))

"""@app_commands.command(name='cum', description="lets you cum on someone's face")
async def cum(self, interaction: discord.Interaction, user):
try:
    
except:
    print('e')"""