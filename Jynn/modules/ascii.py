from discord.ext import commands
import discord
from discord.ext.commands import Cog
import asyncio
import time
import yaml
import math
import ascii


class Art(object):
    def __init__(self, art, tags, artist):
        self.art = art
        self.tags = tags
        self.artist = artist


def load_pending():
    with open("ascii/pending.yaml", "r", encoding="utf8") as pending_file:
        if pending_file.read().strip("\n") == "":
            return []
        pending_file.seek(0)
        pending = yaml.load(pending_file, Loader=yaml.FullLoader)
        return pending


def save_pending(pending):
    with open("ascii/pending.yaml", "w") as pending_file:
        yaml.dump(pending, pending_file)


def load_library():
    with open("ascii/library.yaml", "r", encoding="utf8") as library_file:
        if library_file.read().strip("\n") == "":
            return []
        library_file.seek(0)
        library = yaml.load(library_file.read(), Loader=yaml.FullLoader)
        return library


def save_library(library):
    with open("ascii/library.yaml", "w") as library_file:
        yaml.dump(library, library_file)


class ASCII(Cog):
    """
    ASCII module

    Includes ASCII library and image to ASCII
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group("ascii")
    async def _ascii(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand")

    @_ascii.command(name="search")
    async def _ascii_search(self, ctx, *tags):
        """
        Searches ascii library for given tags
        **tags:** Tags to search for, separated by spaces(tags with spaces must be surrounded by quotes)
        """
        page_msg = await ctx.send("Loading...")

        library = load_library()
        tags = set([x.lower() for x in tags])

        def art_sort(elem):
            a = set([x.lower() for x in elem.tags])
            return len(tags.intersection(a))
        library.sort(key=art_sort)

        library.reverse()

        i = 0
        while i < len(library):
            if art_sort(library[i]) == 0:
                library.pop(i)
            else:
                i += 1

        page = 1
        pages = math.ceil(len(library)/10)

        if len(library) == 0:
            await page_msg.edit(content="No Results")
            return

        while True:
            embed = discord.Embed(title=f"Search Results Page {page}/{pages}")
            i = (page-1)*10
            while i < page * 10 and i < len(library):
                artist_user = self.bot.get_user(library[i].artist)
                if artist_user is None:
                    artist_name = "Submitted by: unknown"
                else:
                    artist_name = f"Submitted by: {artist_user.display_name}#{artist_user.discriminator}"
                embed.add_field(name=library[i].art, value=artist_name, inline=False)
                i += 1
            await page_msg.edit(content="", embed=embed)

            await page_msg.clear_reactions()
            if page > 1:
                await page_msg.add_reaction("⏪")
            if page < pages:
                await page_msg.add_reaction("⏩")
            if pages > 1:
                def check(emoji, user):
                    return user == ctx.author and str(emoji) in ["⏪", "✅", "🏳", "❌", "⏩"]

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                except asyncio.TimeoutError:
                    await page_msg.delete()
                    timeout = await ctx.send("Timed out")
                    time.sleep(10)
                    await timeout.delete()
                    return
                await reaction.remove(user)
                if reaction.emoji == "⏪":
                    page -= 1
                if reaction.emoji == "⏩":
                    page += 1

    @_ascii.command(name="submit")
    async def _ascii_submit(self, ctx):
        """
        Submits ascii art to be reviewed
        """
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
        await reaction.remove(user)
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

    @_ascii.command(name="review")
    async def _ascii_review(self, ctx):
        """
        Reviews submitted ascii art
        """
        pending = load_pending()
        i = 0
        msg = await ctx.send("Loading...")
        while len(pending) > 0:
            embed = discord.Embed(title=f"Pending art {i+1}/{len(pending)}")
            if i > len(pending) - 1:
                i -= 1
            item = pending[i]
            embed.add_field(name="Art:", value=item.art)
            embed.add_field(name="Tags:", value=", ".join(item.tags))
            artist_user = self.bot.get_user(item.artist)
            if artist_user is None:
                artist_name = "unknown"
            else:
                artist_name = f"Submitted by: {artist_user.display_name}#{artist_user.discriminator}"
            embed.add_field(name="Artist:", value=artist_name)
            await msg.edit(content="", embed=embed)

            await msg.clear_reactions()
            if i > 0:
                await msg.add_reaction("⏪")
            await msg.add_reaction("✅")
            await msg.add_reaction("🏳")
            await msg.add_reaction("❌")
            if i < len(pending)-1:
                await msg.add_reaction("⏩")

            def check(emoji, user):
                return user == ctx.author and str(emoji) in ["⏪", "✅", "🏳", "❌", "⏩"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            except asyncio.TimeoutError:
                await msg.delete()
                timeout = await ctx.send("Timed out")
                time.sleep(10)
                await timeout.delete()
                return
            await reaction.remove(user)
            if reaction.emoji == "⏪" and i > 0:
                i -= 1
            if reaction.emoji == "✅":
                library = load_library()
                library.append(item)
                save_library(library)
                pending.pop(i)
                save_pending(pending)
            if reaction.emoji == "🏳":
                report_embed = discord.Embed(title=f"Flagging art")
                report_embed.add_field(name="Are you sure you want to flag", value=item.art, inline=False)
                report_embed.add_field(name="Tags:", value=", ".join(item.tags), inline=False)
                report_embed.add_field(name="Submitted by:", value=f"{artist_user.display_name}#{artist_user.discriminator}", inline=False)
                await msg.edit(embed=report_embed)

                def check(emoji, user):
                    return user == ctx.author and str(emoji) in ["✅", "❌"]

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                except asyncio.TimeoutError:
                    await msg.delete()
                    timeout = await ctx.send("Timed out")
                    time.sleep(10)
                    await timeout.delete()
                    return
                if reaction.emoji == "✅":
                    pass
                if reaction.emoji == "❌":
                    pass
            if reaction.emoji == "❌":
                pending.pop(i)
                save_pending(pending)
            if reaction.emoji == "⏩" and i < len(pending) - 1:
                i += 1
        await msg.edit(content="No more pending ascii art", embed=None)
        await msg.clear_reactions()

    @commands.command(name="convert")
    async def _convert(self, ctx):
        """
        Converts an image to ascii
        *An image must be included as an attachment*
        """
        if len(ctx.message.attachments) == 0:
            await ctx.send("Missing an image to convert")
            return
        output = ascii.loadFromUrl(ctx.message.attachments[0].url, columns=40, color=False)
        print(output)
        await ctx.send(f"```{output}```")


def setup(bot):
    bot.add_cog(ASCII(bot))
