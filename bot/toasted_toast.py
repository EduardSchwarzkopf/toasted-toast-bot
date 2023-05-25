import os
from typing import Optional, Union

from discord import Colour, Embed
from discord.ext import commands


class ToastedToast(commands.Bot):
    def __init__(self, command_prefix, intents, log_channel_id: Optional[int] = None):
        super().__init__(command_prefix, intents=intents)
        self.log_channel_id = log_channel_id

    async def on_ready(self):
        print(
            "Logged in as {0.name} (id: {0.id}), in {1} servers!".format(
                self.user, len(self.guilds)
            )
        )

    async def setup_hook(self):
        cogs_dir = os.path.join(os.path.dirname(__file__), "../cogs")

        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        await self.tree.sync()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await self.send_error(
                ctx.channel.id, f"Command '{ctx.message.content}' not found."
            )

            command_list = [f"{command}" for command in self.commands]
            command_str = "\n".join(command_list)

            await self.send_info(ctx.channel.id, f"Available commands: \n{command_str}")
        else:
            print(f"Unhandled error: {error}")
            await self.send_error(ctx.channel.id, error, "Unexpected error occurred")
        return

    async def manage_cog(self, ctx, extension: Optional[str], action: str):
        if not extension:
            await self.send_error(
                ctx.channel.id, f"You must specify the extension to {action}!"
            )
            return

        try:
            if action in {"unload", "reload"}:
                await self.unload_extension(f"cogs.{extension}")
            if action in {"load", "reload"}:
                await self.load_extension(f"cogs.{extension}")
            title = f":white_check_mark: Command {action} complete"
            description = f"{action.capitalize()}ed {extension}!"
            await self.send_success(
                ctx.channel.id, title=title, description=description, message=""
            )
        except commands.ExtensionNotFound:
            await self.send_error(
                ctx.channel.id, f"No extension named {extension} found!"
            )

    async def send_embed(
        self,
        channel_id: int,
        title: str,
        description: str,
        message: str,
        field_title: str,
        color: Optional[Union[int, Colour]] = 0x84E1BC,
    ) -> None:
        channel = self.get_channel(channel_id)
        embedVar = Embed(title=title, description=description, color=color)
        embedVar.add_field(name=field_title, value=message, inline=False)
        await channel.send(embed=embedVar)

    async def send_error(
        self,
        channel_id: int,
        message: str,
        title: str = ":red_circle: Error",
        description: str = "",
        field_title: str = "",
    ) -> None:
        await self.send_embed(
            channel_id, title, description, message, field_title, color=0xF05252
        )

    async def send_warning(
        self,
        channel_id: int,
        title: str = ":yellow_circle: Warning",
        description: str = "",
        message: str = "",
        field_title: str = "",
    ) -> None:
        await self.send_embed(
            channel_id, title, description, message, field_title, color=0xFACA15
        )

    async def send_success(
        self,
        channel_id: int,
        title: str = ":green_circle: Success",
        description: str = "",
        message: str = "",
        field_title: str = "",
    ) -> None:
        await self.send_embed(
            channel_id, title, description, message, field_title, color=0x84E1BC
        )

    async def send_info(
        self,
        channel_id: int,
        message: str,
        title: str = ":blue_circle: Info",
        description: str = "",
        field_title: str = "",
    ) -> None:
        await self.send_embed(
            channel_id, title, description, message, field_title, color=0xA4CAFE
        )

    async def log_message(
        self,
        message: str,
        message_type: str,
        title: str = "",
        description: str = "",
        field_title: str = "",
    ) -> None:
        if self.log_channel_id is not None:
            colors = {
                "error": 0xF05252,  # Red
                "warning": 0xFACA15,  # Yellow
                "success": 0x84E1BC,  # Green
                "info": 0xA4CAFE,  # Blue
            }
            await self.send_embed(
                self.log_channel_id,
                title,
                description,
                message,
                field_title,
                color=colors[message_type],
            )
