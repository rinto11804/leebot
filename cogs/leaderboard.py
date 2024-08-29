import discord
import os
from discord.ext.commands import Cog, Bot
from discord import app_commands
from database.user_query import UserQuery
from database.room_query import RoomQuery


LEADERBOARD_CHANNEL = int(os.getenv("LEADERBOARD_CHANNEL"))
LEETCODE_ROOM_ID = str(os.getenv("LEETCODE_ROOM_ID"))


class LeaderBoardCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = bot.db
        self.room_query = RoomQuery(self.db)
        self.user_query = UserQuery(self.db)

    @app_commands.command(name="leaderboard", description="generate leaderboard")
    async def add_task(self, interaction: discord.Interaction):
        if interaction.channel.id != LEADERBOARD_CHANNEL:
            return await interaction.response.send_message(
                f"To generate leaderboard, please use the /leaderboard command in the <#{str(LEADERBOARD_CHANNEL)}> channel.",
                delete_after=10,
            )
        user = self.user_query.get_user_by_discord_id(interaction.user.id)
        if not user:
            return await interaction.response.send_message(
                "you are not register",
                delete_after=5,
                ephemeral=True,
            )

        leaderboard = self.room_query.generate_leaderboard(LEETCODE_ROOM_ID)

        embed = discord.Embed(title="🏆 Leaderboard 🏆", color=discord.Color.gold())

        if leaderboard:
            embed.add_field(
                name="🥇 1st Place",
                value=f"**{leaderboard[0]['username']}** - {leaderboard[0]['points']} points",
                inline=False,
            )

        if len(leaderboard) > 1:
            embed.add_field(
                name="🥈 2nd Place",
                value=f"**{leaderboard[1]['username']}** - {leaderboard[1]['points']} points",
                inline=False,
            )

        for index, data in enumerate(leaderboard[2:], start=3):
            embed.add_field(
                name="",
                value=f"{index}. {data['username']} - {data['points']} points",
                inline=False,
            )

        if not leaderboard:
            embed.description = "No data available to display."
        return await interaction.response.send_message(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(LeaderBoardCog(bot))
