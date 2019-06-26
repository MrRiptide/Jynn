from discord.ext import commands
import os
import data

bot = commands.Bot(command_prefix="!")


global first_launch
first_launch = True


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    if first_launch:
        load_modules()


# Helper function to load modules
modules = []


def load_modules():
    global firstLaunch
    for module in os.listdir("modules"):
        if module.endswith(".py"):
            module = module.rstrip("py").rstrip(".")
            try:
                bot.load_extension(f"modules.{module}")
                modules.append(module)
                print(f"Successfully loaded module {module}")
            except Exception as error:
                exc = "{0}: {1}".format(type(error).__name__, error)
                print(f"Failed to load module {module}:\n    {exc}")
    firstLaunch = False


bot.run(data.get_token())
