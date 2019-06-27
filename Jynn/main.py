from discord.ext import commands
import discord
import config
import os
import traceback


class Jynn(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.PREFIX),
            reconnect=True,
        )

        self.config = config

        modules = []

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                modules.append("modules." + file.rstrip("py").rstrip("."))

        for module in modules:
            try:
                self.load_extension(module)
                print(f"Success - {module}")
            except Exception as error:
                exc = f"{type(error).__name__}: {error}"
                print(f"Failure - {module}:\n\n{exc}")

    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if hasattr(ctx.command, 'on_error'):
            return
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"The command `{ctx.command}` is disabled.")
        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"The command `{ctx.message.clean_content}` was not found.")
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"The command `{ctx.command}` is on cooldown, try again in {round(error.retry_after, 2)}s.")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"You missed the parameter `{error.param}`.")
        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send(f"Too many arguments were passed for the command `{ctx.command}`.")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f"A bad argument was passed to the command `{ctx.command}`.")
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"You dont have the permissions to run the `{ctx.command}` command.")
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f"I am missing the following permissions to run the command `{ctx.command}`.\n{error.missing_perms}")
        elif isinstance(error, discord.HTTPException):
            if isinstance(error, discord.Forbidden):
                return await ctx.send(f"I am missing permissions to run the command `{ctx.command}`.")
        elif isinstance(error, commands.CommandInvokeError):
            return await ctx.send(f"There was an error while running the command `{ctx.command}`.")
        else:
            try:
                print(f'{error.original.__class__.__name__}: {error.original}')
                traceback.print_tb(error.original.__traceback__)
            except AttributeError:
                print(f'{error.__class__.__name__}: {error}')
                traceback.print_tb(error.__traceback__)

    async def on_ready(self):
        print(f"\nLogged in as {self.user} - {self.user.id}")

    async def bot_start(self):
        await self.login(config.TOKEN)
        await self.connect()

    async def bot_logout(self):
        await super().logout()

    def run(self):
        loop = self.loop
        try:
            loop.run_until_complete(self.bot_start())
        except KeyboardInterrupt:
            loop.run_until_complete(self.bot_logout())


Jynn().run()
