import discord
from discord.ext import commands


class cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="load",
        brief="Loads an extension",
        description="Loads an extension. You must specify the extension to load. This command can only be run by the bot owner.",
    )
    @commands.is_owner()
    async def load(
        self,
        ctx,
        extension: str = commands.parameter(
            default=None, description=": The name of the extension to load"
        ),
    ):
        await self.bot.manage_cog(ctx, extension, "load")

    @commands.command(
        name="reload",
        brief="Reloads an extension",
        description="Reloads an extension. You must specify the extension to reload. This command can only be run by the bot owner.",
    )
    @commands.is_owner()
    async def reload(
        self,
        ctx,
        extension: str = commands.parameter(
            default=None, description=": The name of the extension to reload"
        ),
    ):
        await self.bot.manage_cog(ctx, extension, "reload")

    @commands.command(
        name="unload",
        brief="Unloads an extension",
        description="Unloads an extension. You must specify the extension to unload. This command can only be run by the bot owner.",
    )
    @commands.is_owner()
    async def unload(
        self,
        ctx,
        extension: str = commands.parameter(
            default=None, description=": The name of the extension to reload."
        ),
    ):
        await self.bot.manage_cog(ctx, extension, "unload")

    @commands.command(name="sync", description="Owner only")
    @commands.is_owner()
    async def sync(self, ctx: discord.Interaction):
        print("Command tree sync started")
        await self.bot.tree.sync()
        msg = "Command tree synced."
        await self.bot.log_message(msg)
        print(msg)


async def setup(bot: commands.Bot):
    await bot.add_cog(cmd(bot))
