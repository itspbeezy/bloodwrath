import discord
from discord.ext import commands
from discord import app_commands

class TestDM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="testdm", description="Test if the bot can send a DM to a user.")
    @app_commands.checks.has_permissions(administrator=True)  # Optional: restrict to administrators
    async def testdm(self, interaction: discord.Interaction, user: discord.Member):
        """Slash command to test DM functionality."""
        try:
            await user.send("This is a test message from the bot.")
            await interaction.response.send_message(f"Test DM sent to {user.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                f"I couldn't send a DM to {user.mention}. Please check their privacy settings.",
                ephemeral=True,
            )
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred: {e}", ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(TestDM(bot))
