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
            overlay = Image.open('folder/img_res/cum.png')
            overlay = overlay.convert("RGBA")
            bg_path = f"folder/img_temp/{uid}.png"
            bg = Image.open(bg_path)
            if bg.size != (256, 256):
                _resize_png(bg_path)
                bg = Image.open(bg_path)
            bg.paste(overlay, (0, 0), mask = overlay)
            bg.save(f'folder/img_temp/{uid}.png')
        
        def _cum_gif(uid):
            overlay = Image.open('folder/img_res/cum.png')
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
    
    @commands.command()
    async def new_cum(self, ctx, user):
        
        def _resize(img):
            i = Image.open(img)
            if i.size != (256, 256):
                i = i.resize((256, 256), Image.Resampling.LANCZOS)
                i.save(img)

        def _cum(img):
            res_path = 'folder/img_res/'
            cums = [Image.open(res_path+'cum1.png'), Image.open(res_path+'cum2.png'), Image.open(res_path+'cum3.png'), Image.open(res_path+'cum4.png'), Image.open(res_path+'cum4.png'), Image.open(res_path+'cum4.png')]
            frames = []
            i = Image.open(img)
            for cum in cums:
                i = i.copy()
                i.paste(cum, (0, 0), mask=cum)
                frames.append(i)
            frames[0].save(img[:-4]+'.gif', save_all=True, append_images=frames[1:], loop=0)


        e = discord.Embed(title='someone has cummed!!!!!!', description=f'fresh semen produced by {ctx.author.mention}', color=discord.Color.pink())
        u: discord.User = discord.utils.get(ctx.guild.members, name=user)
        if u is None:
            u = ctx.author
            e = discord.Embed(title='uoooohh ooh fuuuukkk', description=f'{ctx.author.mention} just cummed on himself !!!11!111!1!1', color=discord.Color.pink())
        await u.avatar.save(f'folder/img_temp/{u.id}.png')
        bg_path = f'folder/img_temp/{u.id}.png'
        _resize(bg_path)
        _cum(bg_path)
        
        file = discord.File(bg_path[:-4]+'.gif', filename=str(u.id)+'.gif')
        e.set_image(url=f'attachment://{u.id}.gif')
        await ctx.channel.send(file=file, embed=e)
        os.remove(bg_path)
        os.remove(bg_path[:-4]+'.gif')
        
async def setup(bot):
    await bot.add_cog(my_bot_Image(bot))