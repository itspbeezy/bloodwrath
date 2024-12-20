import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class AttendanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="attendance", description="Log attendance of all members in voice channels")
    async def log_attendance(self, interaction: discord.Interaction):
        """Log attendance of all members in voice channels."""
        embed = discord.Embed(
            title="Attendance Report",
            description=f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.green()
        )

        for vc in interaction.guild.voice_channels:
            members = vc.members
            if members:
                member_list = "\n".join([f"- {member.display_name}" for member in members])
                embed.add_field(name=vc.name, value=member_list, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AttendanceCog(bot))