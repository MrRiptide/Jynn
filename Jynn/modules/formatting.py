from discord.ext import commands
import pyfiglet
import asyncio
import discord
import math
import os
import re


normal = """`1234567890-=qwertyuiop[]\/asdfghjkl;'zxcvbnm,.~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>? """
king_james = """`1234567890-=𝔮𝔴𝔢𝔯𝔱𝔶𝔲𝔦𝔬𝔭[]\/𝔞𝔰𝔡𝔣𝔤𝔥𝔧𝔨𝔩;'𝔷𝔵𝔠𝔳𝔟𝔫𝔪,.~!@#$%^&*()_+𝔔𝔚𝔈ℜ𝔗𝔜𝔘ℑ𝔒𝔓{}|𝔄𝔖𝔇𝔉𝔊ℌ𝔍𝔎𝔏:"ℨ𝔛ℭ𝔙𝔅𝔑𝔐<>? """
cursive = """`𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢-=𝓆𝓌𝑒𝓇𝓉𝓎𝓊𝒾𝑜𝓅[]\/𝒶𝓈𝒹𝒻𝑔𝒽𝒿𝓀𝓁;'𝓏𝓍𝒸𝓋𝒷𝓃𝓂,.~!@#$%^&*()_+𝒬𝒲𝐸𝑅𝒯𝒴𝒰𝐼𝒪𝒫{}|𝒜𝒮𝒟𝐹𝒢𝐻𝒥𝒦𝐿:"𝒵𝒳𝒞𝒱𝐵𝒩𝑀<>? """
hollow = """`𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘-=𝕢𝕨𝕖𝕣𝕥𝕪𝕦𝕚𝕠𝕡[]\/𝕒𝕤𝕕𝕗𝕘𝕙𝕛𝕜𝕝;'𝕫𝕩𝕔𝕧𝕓𝕟𝕞,.~!@#$%^&*()_+ℚ𝕎𝔼ℝ𝕋𝕐𝕌𝕀𝕆ℙ{}|𝔸𝕊𝔻𝔽𝔾ℍ𝕁𝕂𝕃:"ℤ𝕏ℂ𝕍𝔹ℕ𝕄<>? """
box = """`1234567890-=🆀🆆🅴🆁🆃🆈🆄🅸🅾🅿[]\/🅰🆂🅳🅵🅶🅷🅹🅺🅻;'🆉🆇🅲🆅🅱🅽🅼,.~!@#$%^&*()_+🆀🆆🅴🆁🆃🆈🆄🅸🅾🅿{}|🅰🆂🅳🅵🅶🅷🅹🅺🅻:"🆉🆇🅲🆅🅱🅽🅼<>? """
small = """`¹²³⁴⁵⁶⁷⁸⁹⁰⁻⁼ᵠʷᵉʳᵗʸᵘᶦᵒᵖ[]\/ᵃˢᵈᶠᵍʰʲᵏˡ;'ᶻˣᶜᵛᵇⁿᵐ,.~ᵎ@#$%^&*⁽⁾_⁺ᵠᵂᴱᴿᵀʸᵁᴵᴼᴾ{}|ᴬˢᴰᶠᴳᴴᴶᴷᴸ:"ᶻˣᶜⱽᴮᴺᴹ<>ˀ """

fonts = {
    "normal": normal,
    "king_james": king_james,
    "cursive": cursive,
    "hollow": hollow,
    "box": box,
    "small": small
}


class Formatting(commands.Cog):
    """
    Text formatting plugin

    Includes fonts and other formatting options
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="format")
    async def _format(self, ctx, *, param):
        """
        Formats given phrase in a variety of ways
            **param:** Broken into phrase and formatting_options based on the first tag
            **phrase:** Phrase to format, multi-word phrases must be surrounded by quotes
            **formatting_options:** List of options to format with

            **Formatting options:**
            -upper: Converts phrase to uppercase
            -lower: Converts phrase to lowercase(takes priority over -upper)
            -font: Gives phrase a given font(king_james, cursive, hollow, box, small)(default: cursive)
            -echo: Repeats each letter a given number of times(default: 3)
            -repeat: Repeats the entire phrase a given number of times(default: 2)
            -spaces: Inserts a given number of spaces between each character(default: 1)
            -spoilereach: Marks each character as a spoiler(caution: incompatible with -spoiler)
            -italics: Gives entire phrase italics effect
            -bold: Gives entire phrase bold effect
            -underline: Gives entire phrase underline effect
            -spoiler: Marks entire phrase as a spoiler(caution: incompatible with -spoilereach)
        """
        try:
            tag_start = param.index(" -") + 1
        except ValueError:
            ctx.send("No formatting options provided, use !help format for assistance on this command")
            return
        options = param[tag_start:]
        formatting_options = options.split(" ")
        phrase = param[:tag_start]
        print(options)
        print(formatting_options)
        print(phrase)
        if "-upper" in formatting_options:
            phrase = phrase.upper()
        if "-lower" in formatting_options:
            phrase = phrase.lower()
        if "-font" in formatting_options:
            font = get_argument(formatting_options, "-font", "cursive")
            temp = ""
            try:
                for c in phrase:
                    temp += fonts[font][normal.index(c)]
            except KeyError:
                await ctx.send("Font chosen does not exist")
                raise KeyError("Font chosen does not exist")
            phrase = temp
        if "-echo" in formatting_options:
            try:
                echos = int(get_argument(formatting_options, "-echo", 3))
            except TypeError or ValueError:
                echos = 3
            temp = ""
            for c in phrase:
                temp += c*echos
            phrase = temp
        if "-repeat" in formatting_options:
            try:
                repeats = int(get_argument(formatting_options, "-repeat", 2))
            except TypeError or ValueError:
                repeats = 2
            phrase = phrase*repeats
        if "-spaces" in formatting_options:
            try:
                spaces = int(get_argument(formatting_options, "-spaces", 1))
            except TypeError or ValueError:
                spaces = 1
            temp = " " * spaces
            phrase = temp.join(phrase)
        if "-spoilereach" in formatting_options:
            temp = ""
            for c in phrase:
                temp += f"||{c}||"
            phrase = temp
        if "-italics" in formatting_options:
            phrase = f"*{phrase}*"
        if "-bold" in formatting_options:
            phrase = f"**{phrase}**"
        if "-underline" in formatting_options:
            phrase = f"__{phrase}__"
        if "-spoiler" in formatting_options and "-spoilereach" not in formatting_options:
            phrase = f"||{phrase}||"
        await ctx.send(phrase)
        await ctx.send(f"```{phrase}```")

    @commands.command(name="font")
    async def _font(self, ctx, font, *, phrase):
        """
        Changes entire phrase to a given large font
        **font:** Font to use, fonts can be found using the !fonts command
        **phrase:** Phrase to change font of
        """
        try:
            new_phrase = pyfiglet.figlet_format(phrase, font)
        except pyfiglet.FontNotFound:
            return await ctx.send(f'The font `{font}` was not found.')
        output = ""
        for line in new_phrase.splitlines():
            output += f"\u200B{line}\u200B\n"
        if len(output) > 2000:
            return await ctx.send('The text generated was too long for discord.')
        return await ctx.send(f'```\n{output}```')

    @commands.command(name="fonts")
    async def _fonts(self, ctx, page=1):
        """
        Returns a list of fonts that can be used in the !font command
        **page:** Page to view(default: 1)
        """
        fonts = []
        for file in os.listdir("../venv/Lib/site-packages/pyfiglet/fonts"):
            if file.endswith(".flf"):
                font = ""
                for c in file.rstrip("flf").rstrip("."):
                    if not c.isalnum():
                        font += "\ ".rstrip(" ")
                    font += c
                fonts.append(font)

        if page < 1 or page > math.ceil(len(fonts) / 20):
            page = 1

        msg = await ctx.send(embed=gen_font_page(fonts, page))
        await msg.add_reaction("⏮")
        await msg.add_reaction("⏪")
        await msg.add_reaction("⏩")
        await msg.add_reaction("⏭")

        while True:
            def check(emoji, user):
                return user == ctx.author and str(emoji) in ["⏮", "⏪", "⏩", "⏭"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            except asyncio.TimeoutError:
                break
            if reaction.emoji == "⏮":
                page = 1
            if reaction.emoji == "⏪" and page > 1:
                page -= 1
            if reaction.emoji == "⏩" and page < math.ceil(len(fonts) / 20):
                page += 1
            if reaction.emoji == "⏭":
                page = math.ceil(len(fonts) / 20)

            await reaction.remove(user)

            await msg.edit(embed=gen_font_page(fonts, page))

    @commands.command(name="owoify", aliases=['owo', 'uwu'])
    async def _owo(self, ctx, *, statement):
        """
        Owo-ifies a statement
        **statement:** Statement to owoify
        """
        statement = replace_keep_case("l", "w", statement)
        statement = replace_keep_case("r", "w", statement)
        statement = replace_keep_case("ove", "uv", statement)
        statement = replace_keep_case("na", "nya", statement)
        statement = replace_keep_case("ne", "nye", statement)
        statement = replace_keep_case("ni", "nyi", statement)
        statement = replace_keep_case("no", "nyo", statement)
        statement = replace_keep_case("nu", "nyu", statement)
        await ctx.send(statement)


def gen_font_page(fonts, page):
    i = (page - 1) * 20
    embed = discord.Embed(title=f"Page {page}/{math.ceil(len(fonts) / 20)}")
    while i < page * 20 and i < len(fonts):
        if i + 1 == len(fonts):
            embed.add_field(name=fonts[i], value="\u200B", inline=False)
        else:
            embed.add_field(name=fonts[i], value=fonts[i + 1], inline=False)
        i += 2
    return embed


def replace_keep_case(word, replacement, text):
    def func(match):
        g = match.group()
        if g.islower():
            return replacement.lower()
        if g.istitle():
            return replacement.title()
        if g.isupper():
            return replacement.upper()
        return replacement
    return re.sub(word, func, text, flags=re.I)


def get_argument(options, attribute, default):
    try:
        argument = options[options.index(attribute) + 1]
    except IndexError:
        return default
    if argument.startswith("-"):
        return default
    return argument


def setup(bot):
    bot.add_cog(Formatting(bot))
    """cmd = bot.get_command("format")
    cmd.signature = "<phrase> [formatting_options...]"
    bot.remove_command("format")
    bot.add_command(cmd)"""
