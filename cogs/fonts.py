from discord.ext import commands
import json

def convert_font(message: tuple[str], font: str):
        with open('fonts.json', 'r') as jfile:
            f = json.load(jfile)[f"{font}"]
        m = ' '.join(message)
        t = []
        for c in m:
            if c.isalpha():
                t.append(f[f"{c}"])
            else:
                t.append(c)
        return ''.join(t)

class myBotFont(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def fonts(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            pass
    
    @fonts.command()
    async def smallcaps(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='small caps')
        await ctx.send(m)
    
    @fonts.command()
    async def boldfractur(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='bold fractur')
        await ctx.send(m)
    
    @fonts.command()
    async def boldcircle(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='bold circle')
        await ctx.send(m)
    
    @fonts.command()
    async def monospace(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='mono space')
        await ctx.send(m)

    @fonts.command()
    async def superscript(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='superscript')
        await ctx.send(m)

    @fonts.command()
    async def cursive(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message.content, font='cursive')
        await ctx.send(m)

    @fonts.command()
    async def boldscript(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='bold script')
        await ctx.send(m)

    @fonts.command()
    async def SBI(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='sans bold italic')
        await ctx.send(m)

    @fonts.command()
    async def upsidedown(self, ctx:commands.Context ,*message: str):
        m = convert_font(message=message, font='upside down')
        await ctx.send(m)

async def setup(bot):
    await bot.add_cog(myBotFont(bot=bot))