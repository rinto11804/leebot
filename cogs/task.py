import discord
import os
from discord.ext.commands import Cog, Bot
from database.task_query import TaskQuery
from database.user_query import UserQuery
from database.answer_query import AnswerQuery
from database.room_query import RoomQuery
from type import User, Roles, Task, AnswerAlreadyCorrectedError, AnswerNotFoundError

TASK_CHANNEL = int(os.getenv("TASK_CHANNEL"))
LEETCODE_ROOM_ID = str(os.getenv("LEETCODE_ROOM_ID"))


class TaskCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = bot.db
        self.task_query = TaskQuery(self.db)
        self.room_query = RoomQuery(self.db)
        self.user_query = UserQuery(self.db)
        self.answer_query = AnswerQuery(self.db)
        self.user: User = None

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await self.mark_answer(payload)

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.type is not discord.ChannelType.text:
            return

        self.user = self.user_query.get_user_by_discord_id(message.author.id)
        if not self.user:
            return await message.reply("User not found", delete_after=5)

        if message.channel.id == TASK_CHANNEL:
            await self.add_answer(message)

    async def add_answer(self, message: discord.Message):
        if not message.content.startswith("#"):
            return await message.reply("This is not a  valid hashtag", delete_after=5)

        question_no = message.content.split("#")[1]
        if question_no == "":
            return await message.reply(
                "This is not a  have valid hashtag", delete_after=5
            )

        task = self.task_query.is_task_valid(LEETCODE_ROOM_ID, message.content)
        if not task:
            return await message.reply(
                "Task with this hashtag does not exist", delete_after=5
            )

        if not self.answer_query.create_answer(message.id, task.id, self.user.id):
            return await message.reply(
                "Answer submitted is not accepted", delete_after=5
            )

        return await message.reply("answer submitted successfully", delete_after=5)

    async def mark_answer(self, payload: discord.RawReactionActionEvent):
        channel = self.bot.get_channel(payload.channel_id)
        member_id = payload.user_id
        message_id = payload.message_id
        member = await self.bot.get_guild(payload.guild_id).fetch_member(member_id)
        message = await channel.fetch_message(message_id)
        emoji = payload.emoji.name
        task: Task = self.task_query.get_task(LEETCODE_ROOM_ID, message.content)

        if emoji != "✅":
            return await message.remove_reaction(emoji, member)
        user = self.user_query.get_user_by_discord_id(payload.member.id)
        if not user:
            await message.remove_reaction(emoji, member)
            return await payload.member.send("You cant react to the answer")

        if Roles.ADMIN.value not in user.roles:
            await message.remove_reaction(emoji, member)
            return await payload.member.send("You cant react to the answer")
        try:
            res = self.answer_query.mark_answer_as_correct(message_id, user.id)
        except (AnswerAlreadyCorrectedError, AnswerNotFoundError) as e:
            return await message.reply(e.message, delete_after=10)
        if not res:
            await message.remove_reaction(emoji, member)
            return await payload.member.send(
                "Something went wrong answer not corrected"
            )
        if not self.room_query.grant_point(LEETCODE_ROOM_ID, user.id, task.points):
            await message.remove_reaction(emoji, member)
            return await payload.member.send(
                "Something went wrong answer not corrected"
            )
        return await payload.member.send(
            f"Congratulations 🎉, your answer is validated and accepted, Good Job <@{str(member_id)}>"
        )


async def setup(bot: Bot):
    await bot.add_cog(TaskCog(bot))
