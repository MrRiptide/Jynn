from discord.ext import commands
import config


modules = [
    'modules.formatting',
    'jishaku'
]


class Jynn(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.PREFIX),
            reconnect=True,
        )

        self.config = config

        for module in modules:
            try:
                self.load_extension(module)
                print(f"Success - {module}")
            except Exception as error:
                exc = f"{type(error).__name__}: {error}"
                print(f"Failure - {module}:\n\n{exc}")

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
