import discord
import os
from type import User
from discord import app_commands
from database.user_query import UserQuery
from database.room_query import RoomQuery
from discord.ext.commands import Cog, Bot

ONBOARD_CHANNEL = int(os.getenv("ONBOARD_CHANNEL"))
LEETCODE_ROOM_ID = str(os.getenv("LEETCODE_ROOM_ID"))


class Register(discord.ui.Modal, title="Join Form"):
    email = discord.ui.TextInput(label="Email", placeholder="Your email id here...")

    def __init__(self):
        super().__init__(timeout=0)
        self.user_query = UserQuery()
        self.room_query = RoomQuery()

    async def on_submit(self, interaction: discord.Interaction):
        # email = interaction.data.get("components").get("value")
        email = interaction.data.get("components")[0].get("components")[0].get("value")
        discord_id = interaction.user.id

        user: User = self.user_query.get_user_by_email(email)
        if not user:
            return await interaction.response.send_message(
                "You are not registered, join when you are register with this email",
                delete_after=10,
            )
        if not self.user_query.add_discord_id(user.id, discord_id):
            return await interaction.response.send_message(
                "Failed to load the discord id", delete_after=10
            )
        res = self.room_query.join_room(LEETCODE_ROOM_ID, user.id)
        if not res:
            return await interaction.response.send_message(
                "Opps! Someting went wrong, please join again",
                delete_after=10,
            )
        return await interaction.response.send_message(
            "Welcome to Leetcode Practice", ephemeral=True
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        return await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )


class IntroCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    @app_commands.command(name="join", description="registe and join room")
    async def feedback(self, interaction: discord.Interaction):
        if interaction.channel.id != ONBOARD_CHANNEL:
            return await interaction.response.send_message(
                f"To join, please use the /join command in the <#{str(ONBOARD_CHANNEL)}> channel.",
                delete_after=10,
            )

        await interaction.response.send_modal(Register())


async def setup(bot: Bot):
    await bot.add_cog(IntroCog(bot))
