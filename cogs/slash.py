import discord
from discord.ext import commands
from discord import app_commands


class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
