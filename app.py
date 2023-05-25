import os
import discord
from dotenv import load_dotenv
from bot.toasted_toast import ToastedToast

load_dotenv()

LOGGING_CHANNEL_ID = int(os.getenv("LOGGING_CHANNEL_ID"))

intents = discord.Intents.all()

bot = ToastedToast(
    command_prefix="$", intents=intents, log_channel_id=LOGGING_CHANNEL_ID
)

bot.run(os.environ.get("DISCORD_TOKEN"))
