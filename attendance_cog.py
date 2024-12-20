import discord
from discord.ext import commands
from datetime import datetime
import pytz

class AttendanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="attendance")
    @commands.has_permissions(administrator=True)
    async def log_attendance(self, ctx):
        """Log attendance of all members in voice channels."""
        embed = discord.Embed(
            title="Attendance Report",
            description=f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.green()
        )

        for vc in ctx.guild.voice_channels:
            members = vc.members
            if members:
                member_list = "\n".join([f"- {member.display_name}" for member in members])
                embed.add_field(name=vc.name, value=member_list, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AttendanceCog(bot))
