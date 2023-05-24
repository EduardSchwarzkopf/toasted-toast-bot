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
async def on_ready():
    await bot.tree.sync()
    print(
        "Logged in as {0.name} (id: {0.id}), in {1} servers!".format(
            bot.user, len(bot.guilds)
        )
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


@bot.command(
    name="load",
    brief="Loads an extension",
    description="Loads an extension. You must specify the extension to load. This command can only be run by the bot owner.",
)
@commands.is_owner()
async def load(
    ctx,
    extension: str = commands.parameter(
        default=None, description=": The name of the extension to load"
    ),
):
    await bot.manage_cog(ctx, extension, "load")


@bot.command(
    name="reload",
    brief="Reloads an extension",
    description="Reloads an extension. You must specify the extension to reload. This command can only be run by the bot owner.",
)
@commands.is_owner()
async def reload(
    ctx,
    extension: str = commands.parameter(
        default=None, description=": The name of the extension to reload"
    ),
):
    await bot.manage_cog(ctx, extension, "reload")


@bot.command(
    name="unload",
    brief="Unloads an extension",
    description="Unloads an extension. You must specify the extension to unload. This command can only be run by the bot owner.",
)
@commands.is_owner()
async def unload(
    ctx,
    extension: str = commands.parameter(
        default=None, description=": The name of the extension to reload."
    ),
):
    await bot.manage_cog(ctx, extension, "unload")


# Read Cogs folder and load them
cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")

for filename in os.listdir(cogs_dir):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(os.environ.get("DISCORD_TOKEN"))
