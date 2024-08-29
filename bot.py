from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
from database.connection import DBConnection

load_dotenv()
TOKEN: str = str(os.getenv("TOKEN"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: DBConnection = DBConnection()

    async def on_ready(self):
        await self.load_extension("cogs.intro")
        await self.load_extension("cogs.task")
        await self.load_extension("cogs.leaderboard")
        await self.tree.sync()
        print(f"{self.user} has connected to Discord!")


bot = CustomBot(command_prefix="/", intents=intents)

bot.run(token=TOKEN)
