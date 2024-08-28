import discord
import os
from discord import app_commands
from discord.ext.commands import Cog, Bot

TASK_CHANNEL = int(os.getenv("TASK_CHANNEL"))
LEETCODE_ROOM_ID = str(os.getenv("LEETCODE_ROOM_ID"))


class TaskCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    @app_commands.command(name="join", description="registe and join room")
    async def feedback(self, interaction: discord.Interaction):
        pass


async def setup(bot: Bot):
    await bot.add_cog(TaskCog(bot))
