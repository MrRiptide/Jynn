from discord.ext import commands
import discord
from discord.ext.commands import Cog
import asyncio
import time
import yaml


class Art(object):
	def __init__(self, art, tags, artist):
		self.art = art
		self.tags = tags
		self.artist = artist


def load_pending():
	with open("ascii/pending.yaml", "r", encoding="utf8") as pending_file:
		if pending_file.read().strip("\n") == "":
			return []
		print(pending_file)
		pending = yaml.load(pending_file, Loader=yaml.FullLoader)
		print(pending)
		return pending


def save_pending(pending):
	pending_file = open("ascii/pending.yaml", "w")
	yaml.dump(pending, pending_file)
	pending_file.close()


def load_library():
	library_file = open("ascii/pending.yaml", "r")
	if library_file.read().strip("\n") == "":
		return []
	library = yaml.load(library_file.read(), Loader=yaml.FullLoader)
	library_file.close()
	return library


def save_library(library):
	library_file = open("ascii/pending.yaml", "w")
	yaml.dump(library, library_file)
	library_file.close()


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
		pass

	@_ascii.command(name="submit")
	async def _ascii_submit(self, ctx):
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

	@_ascii.command(name="review")
	async def _ascii_review(self, ctx):
		pending = load_pending()
		i = 0
		msg = await ctx.send("Loading...")
		while len(pending) > 0:
			embed = discord.Embed(title=f"Pending art {i}/{len(pending)}")
			item = pending[i]
			embed.add_field(name="Art:", value=item.art)
			embed.add_field(name="Tags:", value=", ".join(item.tags))
			artist_user = self.bot.get_user(item.artist)
			artist_name = f"{artist_user.display_name}#{artist_user.discriminator}"
			embed.add_field(name="Artist:", value=artist_name)
			await msg.edit("", embed=embed)

			if i > 0:
				await msg.add_reaction("⏪")
			await msg.add_reaction("✅")
			await msg.add_reaction("❌")
			if i < len(pending) - 1:
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
			if reaction.emoji == "⏪":
				i -= 1
			if reaction.emoji == "✅":
				library = load_library()
				library.append(item)
				save_library(library)
				pending.pop(i)
				temp = await ctx.send("Accepted art")
				time.sleep(5)
				await temp.delete()
			if reaction.emoji == "❌":
				pending.pop(i)
				temp = await ctx.send("Denied art")
				time.sleep(5)
				await temp.delete()
			if reaction.emoji == "⏩":
				i += 1
		save_pending(pending)
		await msg.edit(content="No more pending ascii art")


def setup(bot):
	bot.add_cog(ASCII(bot))