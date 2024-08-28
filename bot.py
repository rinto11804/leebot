from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()
TOKEN: str = str(os.getenv("TOKEN"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    await bot.load_extension("cogs.intro")
    await bot.tree.sync()


bot.run(token=TOKEN)
