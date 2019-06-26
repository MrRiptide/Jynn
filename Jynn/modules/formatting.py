from discord.ext import commands
from discord.ext.commands import Cog
import discord
import pyfiglet
import os
import math
from discord.ext import buttons


class MyPaginator(buttons.Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @buttons.button(emoji='\u23FA')
    async def record_button(self, ctx):
        await ctx.send('This button sends a silly message! But could be programmed to do much more.')

    @buttons.button(emoji='my_custom_emoji:1234567890')
    async def silly_button(self, ctx):
        await ctx.send('Beep boop...')


class Formatting(Cog):
    """
    Text formatting plugin

    Includes fonts and other formatting options
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="format")
    async def _format(self, ctx, phrase, *formatting_options):

        await ctx.send(phrase)

    @commands.command(name="font")
    async def _font(self, ctx, phrase, font):
        new_phrase = pyfiglet.figlet_format(phrase, font)
        output = ""
        for line in new_phrase.splitlines():
            output += f"\u200B{line}\u200B\n"
        output = f"`\n{output}`"
        print(output)
        await ctx.send(output)

    @commands.command(name="fonts")
    async def _fonts(self, ctx, page=1):
        fonts = []
        for file in os.listdir("venv/Lib/site-packages/pyfiglet/fonts"):
            if file.endswith(".flf"):
                fonts.append(file.rstrip("flf").rstrip("."))
        if page < 1 or page > math.ceil(len(fonts) / 20):
            page = 1
        i = (page-1) * 20
        embed = discord.Embed(title=f"Page {page}/{math.ceil(len(fonts) / 20)}")
        while i < page * 20 and i < len(fonts):
            if i+1 == len(fonts):
                embed.add_field(name=fonts[i], value="\u200B", inline=False)
            else:
                embed.add_field(name=fonts[i], value=fonts[i+1], inline=False)
            i += 2
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("⏮")
        await msg.add_reaction("⏪")
        await msg.add_reaction("⏩")
        await msg.add_reaction("⏭")

    @commands.command()
    async def test(ctx):
        pagey = MyPaginator(title='Silly Paginator', colour=0xc67862, embed=True, timeout=90, use_defaults=True,
                            entries=[1, 2, 3], length=1, format='**')

        await pagey.start(ctx)


def setup(bot):
    bot.add_cog(Formatting(bot))
