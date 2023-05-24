from typing import Optional, Union
from enum import Enum

from discord import Colour, Embed
from discord.ext import commands


class MessageType(Enum):
    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"


class ToastedToast(commands.Bot):
    def __init__(self, command_prefix, intents, log_channel_id: Optional[int] = None):
        super().__init__(command_prefix, intents=intents)
        self.log_channel_id = log_channel_id

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
        color: Optional[Union[int, Colour]] = 0x00FF00,
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
            channel_id, title, description, message, field_title, color=0xFF0000
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
            channel_id, title, description, message, field_title, color=0xFFFF00
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
            channel_id, title, description, message, field_title, color=0x00FF00
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
            channel_id, title, description, message, field_title, color=0x0000FF
        )

    async def log_message(
        self,
        message: str,
        message_type: MessageType = MessageType.INFO,
        title: str = "",
        description: str = "",
        field_title: str = "",
    ) -> None:
        if self.log_channel_id is not None:
            colors = {
                MessageType.ERROR: 0xFF0000,  # Red
                MessageType.WARNING: 0xFFFF00,  # Yellow
                MessageType.SUCCESS: 0x00FF00,  # Green
                MessageType.INFO: 0x0000FF,  # Blue
            }
            await self.send_embed(
                self.log_channel_id,
                title,
                description,
                message,
                field_title,
                color=colors[message_type],
            )
