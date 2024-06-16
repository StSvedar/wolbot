from discord.ext import commands
from Utils.Log_manager import Log_manager

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_manager = Log_manager()

    def log(self, message):
        self.log_manager.log(message)

    async def close(self):
        del self.log_manager
        await super().close()