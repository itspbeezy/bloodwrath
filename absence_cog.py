import discord
from discord.ext import commands

class AbsenceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="absence")
    async def absence_report(self, ctx):
        """Submit an absence report."""
        await ctx.send(
            "Use this format to submit your absence:\n"
            "```\nName: [Your Name]\nEvents Missing: [Events]\nDates: [Dates]\nReason: [Reason]\n```"
        )

async def setup(bot):
    await bot.add_cog(AbsenceCog(bot))
