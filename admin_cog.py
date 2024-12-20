import discord
from discord.ext import commands
from discord import app_commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sync", description="Sync all slash commands")
    async def sync_commands(self, interaction: discord.Interaction):
        """Sync all slash commands."""
        try:
            synced = await self.bot.tree.sync()
            await interaction.response.send_message(f"Synced {len(synced)} commands globally.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error syncing commands: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))