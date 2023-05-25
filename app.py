import os
import discord
from dotenv import load_dotenv
from bot.toasted_toast import ToastedToast
from discord.ext import commands
from typing import Optional

load_dotenv()

LOGGING_CHANNEL_ID = int(os.getenv("LOGGING_CHANNEL_ID"))

intents = discord.Intents.all()

bot = ToastedToast(
    command_prefix="$", intents=intents, log_channel_id=LOGGING_CHANNEL_ID
)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await bot.send_error(
            ctx.channel.id, f"Command '{ctx.message.content}' not found."
        )

        command_list = [f"{command}" for command in bot.commands]
        command_str = "\n".join(command_list)

        await bot.send_info(ctx.channel.id, f"Available commands: \n{command_str}")

    else:
        print(f"Unhandled error: {error}")
        await bot.send_error(ctx.channel.id, f"Unexpected error occurred: {error}")
    return


bot.run(os.environ.get("DISCORD_TOKEN"))
