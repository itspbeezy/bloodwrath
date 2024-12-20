import discord
from discord.ext import commands
from discord import app_commands

class AbsenceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="absence", description="Submit an absence report")
    async def absence_report(self, interaction: discord.Interaction):
        """Submit an absence report."""
        await interaction.response.send_message(
            "Use this format to submit your absence:\n"
            "```\nName: [Your Name]\nEvents Missing: [Events]\nDates: [Dates]\nReason: [Reason]\n```",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(AbsenceCog(bot))