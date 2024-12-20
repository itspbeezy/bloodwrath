import discord
from discord.ext import commands
from discord import app_commands

class AbsenceModal(discord.ui.Modal, title="Submit Absence Report"):
    name = discord.ui.TextInput(label="Name", placeholder="Enter your name")
    events = discord.ui.TextInput(label="Events Missing", placeholder="e.g., Guild Boss, Rift Stone")
    dates = discord.ui.TextInput(label="Dates", placeholder="e.g., Dec 20 - Dec 25")
    reason = discord.ui.TextInput(label="Reason", style=discord.TextStyle.paragraph, placeholder="Enter the reason for absence")

    def __init__(self, channel_id):
        super().__init__()
        self.channel_id = channel_id

    async def on_submit(self, interaction: discord.Interaction):
        # Format the absence report
        embed = discord.Embed(
            title="Absence Report Submitted",
            description=(
                f"**Name:** {self.name.value}\n"
                f"**Events Missing:** {self.events.value}\n"
                f"**Dates:** {self.dates.value}\n"
                f"**Reason:** {self.reason.value}"
            ),
            color=discord.Color.blue()
        )

        # Send confirmation to the user
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Send the absence report to the specified channel
        channel = interaction.guild.get_channel(self.channel_id)
        if channel:
            await channel.send(embed=embed)
        else:
            print(f"Channel with ID {self.channel_id} not found.")

class AbsenceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="absent", description="Submit an absence report")
    async def absent(self, interaction: discord.Interaction):
        """Command to open the absence form."""
        # Replace with your desired channel ID
        channel_id = 1317274570914533417
        modal = AbsenceModal(channel_id)
        await interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(AbsenceCog(bot))