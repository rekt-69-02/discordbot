import discord, os
from PIL import Image, ImageSequence
from discord.ext import commands

class my_bot_Image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def cum(self, ctx, user):

        def _resize_png(image: str):
            i = Image.open(image)
            i = i.resize((256, 256), Image.Resampling.LANCZOS)
            i.save(image)

        def _resize_gif(image: str):
            with Image.open(image) as i:
                frames = []
                for frame in ImageSequence.Iterator(i):
                    frame = frame.resize((256, 256))
                    frames.append(frame)
                frames[0].save(image, save_all=True, append_images=frames[1:])

        def _cum_png(uid):
            overlay = Image.open('folder/img_res/cum1.png')
            overlay = overlay.convert("RGBA")
            bg_path = f"folder/img_temp/{uid}.png"
            bg = Image.open(bg_path)
            if bg.size != (256, 256):
                _resize_png(bg_path)
                bg = Image.open(bg_path)
            bg.paste(overlay, (0, 0), mask = overlay)
            bg.save(f'folder/img_temp/{uid}.png')
        
        def _cum_gif(uid):
            overlay = Image.open('folder/img_res/cum1.png')
            overlay = overlay.convert("RGBA")
            bg_path = f"folder/img_temp/{uid}.gif"
            i = Image.open(bg_path)
            if i.size != (256, 256):
                _resize_gif(bg_path)
                i = Image.open(bg_path)
            frames = []
            for frame in ImageSequence.Iterator(i):
                frame = frame.copy()
                frame.paste(overlay, (0, 0), mask=overlay)
                frames.append(frame)
            frames[0].save(bg_path, save_all=True, append_images=frames[1:])

        u: discord.User = discord.utils.find(lambda m: m.name == user, ctx.guild.members)
        e = discord.Embed(title='someone has cumemd!!111!!1!111!11!!1', color=discord.Color.pink())
        if u is None:
            u = ctx.author
            user_not_found = True
            e = discord.Embed(title=f'uoooohh oh fuck **{u.name}** has cummed on himself looooll', color=discord.Color.pink())
        if u.avatar.is_animated():
            bgpath = f"folder/img_temp/{u.id}.gif"
            await u.avatar.save(bgpath)
            _cum_gif(u.id)
            file = discord.File(bgpath, filename=str(u.id)+'.gif')
            e.set_image(url=f'attachment://{u.id}.gif')
            await ctx.channel.send(file=file, embed=e)
            os.remove(bgpath)
        else:
            bgpath = f"folder/img_temp/{u.id}.png"
            await u.avatar.save(bgpath)
            _cum_png(u.id)
            file = discord.File(bgpath, filename=str(u.id)+'.png')
            e.set_image(url=f'attachment://{u.id}.png')
            await ctx.channel.send(file=file, embed=e)
            os.remove(bgpath)
    

async def setup(bot):
    await bot.add_cog(my_bot_Image(bot))