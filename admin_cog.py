import discord
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync_commands(self, ctx):
        """Sync all slash commands."""
        try:
            synced = await self.bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} commands globally.")
        except Exception as e:
            await ctx.send(f"Error syncing commands: {e}")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
