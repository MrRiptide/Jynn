from discord.ext import commands
from discord.ext.commands import Cog
import asyncio
import time
import yaml


class Art(object):
    def __init__(self, art, tags, author):
        self.art = art
        self.tags = tags
        self.author = author


def load_pending():
    pending_file = open("ascii/pending.yaml", "r")
    if pending_file.read().strip("\n") == "":
        return []
    pending = yaml.load(pending_file.read(), Loader=yaml.FullLoader)
    return pending


def save_pending(pending):
    pending_file = open("ascii/pending.yaml", "w+")
    yaml.dump(pending, pending_file)


class ASCII(Cog):
    """
    ASCII module

    Includes ASCII library and image to ASCII
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ascii")
    async def _ascii(self, ctx, subcommand, *tags):
        if subcommand == "search":
            pass
        if subcommand == "submit":
            last = await ctx.send("Enter ascii art:")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                art_message = await self.bot.wait_for("message", check=check, timeout=30)
                art = art_message.content
            except asyncio.TimeoutError:
                await last.delete()
                timeout = await ctx.send("Timed out")
                time.sleep(10)
                await timeout.delete()
                return

            await last.delete()

            last = await ctx.send("Enter tags separated by a comma")

            try:
                tags_message = await self.bot.wait_for("message", check=check, timeout=30)
                tags = tags_message.content.replace(" ", "").split(",")
            except asyncio.TimeoutError:
                await last.delete()
                timeout = await ctx.send("Timed out")
                time.sleep(10)
                await timeout.delete()
                return

            await last.delete()

            confirmation = await ctx.send(f"""Are you sure you want to submit this ascii art?\n
            **Art:**
            {art_message.content}\n
            **Tags:**
            {", ".join(tags)}\n
            React :white_check_mark: to confirm and :x: to cancel.
            """)

            await confirmation.add_reaction("✅")
            await confirmation.add_reaction("❌")

            def check(emoji, user):
                return user == ctx.author and str(emoji) in ["✅", "❌"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            except asyncio.TimeoutError:
                await confirmation.delete()
                timeout = await ctx.send("Timed out")
                time.sleep(10)
                await timeout.delete()
                return
            if reaction.emoji == "✅":
                ascii_art = Art(art, tags, ctx.author.id)
                await confirmation.delete()
                pending = load_pending()
                pending.append(ascii_art)
                save_pending(pending)
                final = await ctx.send("Submitted for review")
                time.sleep(10)
                await final.delete()
                return
            if reaction.emoji == "❌":
                await confirmation.delete()
                cancelled = await ctx.send("Cancelled")
                time.sleep(10)
                await cancelled.delete()
                return


def setup(bot):
    bot.add_cog(ASCII(bot))
