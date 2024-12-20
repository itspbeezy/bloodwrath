import discord
from discord.ext import commands
from datetime import datetime

class ScheduleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="schedule")
    @commands.has_permissions(administrator=True)
    async def post_schedule(self, ctx):
        """Post the guild schedule."""
        embed = discord.Embed(
            title="Guild Schedule",
            description=(
                "**🗡️ PvP all Day every day!!!**\n"
                "Inter-Server Wars are a way for Guilds to fight against other guilds on other servers. "
                "These wars happen every 2 weeks - 48 vs 48 Guild vs Guild battle.\n\n"
                "**🛒 Tax Cart:** Depends on defending guild!"
            ),
            color=discord.Color.dark_red(),
            timestamp=datetime.utcnow()
        )

        # Adding fields for each day of the week
        embed.add_field(
            name="📅 Sunday",
            value="• **Siege:** 5:00 PM EST *(Every other Sunday)*\n"
                  "• **Guild Bosses:** 7:30 PM EST\n"
                  "• **Rift Stone Boss:** After Guild Bosses\n"
                  "• **Conflict Bosses (Alliance):** 8:00 PM & 11:00 PM EST",
            inline=False
        )
        embed.add_field(
            name="📅 Monday",
            value="• **Rift Stone Boss:** 7:30 PM EST\n"
                  "• **Conflict Bosses (Alliance):** 8:00 PM & 11:00 PM EST\n"
                  "• **Boon Stone:** 9:00 PM EST\n"
                  "• **Interserver Stone:** 9:30 PM EST *(Every other week)*",
            inline=False
        )
        embed.add_field(
            name="📅 Tuesday",
            value="• **Rift Stone Boss:** 7:30 PM EST\n"
                  "• **Conflict Bosses (Alliance):** 8:00 PM & 11:00 PM EST\n"
                  "• **Rift Stone:** 9:00 PM EST\n"
                  "• **Interserver Stone:** 9:30 PM EST *(Every other week)*",
            inline=False
        )
        embed.add_field(
            name="📅 Wednesday",
            value="• **Rift Stone Boss:** 7:30 PM EST\n"
                  "• **Conflict Bosses (Alliance):** 8:00 PM & 11:00 PM EST",
            inline=False
        )
        embed.add_field(
            name="📅 Thursday",
            value="• **Guild Bosses:** 7:30 PM EST\n"
                  "• **Rift Stone Boss:** After Guild Bosses\n"
                  "• **Conflict Bosses (Alliance):** 8:00 PM & 11:00 PM EST",
            inline=False
        )
        embed.add_field(
            name="📅 Friday",
            value="• **Rift Stone Boss:** 7:30 PM EST\n"
                  "• **Conflict Bosses (Alliance):** 8:00 PM & 11:00 PM EST\n"
                  "• **Rift Stone:** 9:00 PM EST\n"
                  "• **Interserver Stone:** 9:30 PM EST *(Every other week)*",
            inline=False
        )
        embed.add_field(
            name="📅 Saturday",
            value="• **Rift Stone Boss:** 7:30 PM EST\n"
                  "• **Conflict Bosses (Alliance):** 8:00 PM & 11:00 PM EST\n"
                  "• **Boon Stone:** 9:00 PM EST\n"
                  "• **Interserver Stone:** 9:30 PM EST *(Every other week)*",
            inline=False
        )

        embed.set_footer(text="Last Updated")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ScheduleCog(bot))
