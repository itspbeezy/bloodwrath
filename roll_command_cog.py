import discord
from discord.ext import commands
from discord import app_commands

class GuildInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild_info = {
            "server": "Laslan - Early Access",
            "recruitment_status": "Application Only - Apply at: <#1322470388122390599>",
            "requirements": "4k CP+"
        }

    @app_commands.command(name="post_guild_info", description="Post the guild information to the designated channel.")
    async def post_guild_info(self, interaction: discord.Interaction):
        """Command to post the guild information."""
        channel_id = 1322469415874465824
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            await interaction.response.send_message("The designated channel could not be found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Guild Information",
            description=(
                "Blood Wrath is a hardcore PVP guild looking to dominate the battlefield and contest and conquer "
                "world bosses, arch bosses, boon and riftstone battles and guild PVP events. We also are pushing "
                "limits for Runes and all PVE content."
            ),
            color=discord.Color.red()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1288633288717766706/1320526678337785951/discordserverlogo4.gif?ex=6770834e&is=676f31ce&hm=e836cb4196a478456e281d368b7158671c0e1a03dab8b6fc42ed9275674f9b41&")

        embed.add_field(name="Server", value=self.guild_info["server"], inline=False)
        embed.add_field(name="Recruitment Status", value=self.guild_info["recruitment_status"], inline=False)
        embed.add_field(name="Requirements", value=self.guild_info["requirements"], inline=False)

        await channel.send(embed=embed)
        await interaction.response.send_message("Guild information posted successfully!", ephemeral=True)

    @app_commands.command(name="update_guild_info", description="Update the guild information.")
    @app_commands.describe(
        server="The server name and status.",
        recruitment_status="The recruitment status and application link.",
        requirements="The requirements to join the guild."
    )
    async def update_guild_info(self, interaction: discord.Interaction, server: str, recruitment_status: str, requirements: str):
        """Command to update the guild information."""
        self.guild_info["server"] = server
        self.guild_info["recruitment_status"] = recruitment_status
        self.guild_info["requirements"] = requirements

        await interaction.response.send_message("Guild information updated successfully!", ephemeral=True)

    @app_commands.command(name="post_rules", description="Post the Discord rules to the designated channel.")
    async def post_rules(self, interaction: discord.Interaction):
        """Command to post the Discord rules."""
        channel_id = 1235798906382585909
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            await interaction.response.send_message("The designated channel could not be found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="SERVER RULES",
            description=(
                "**Rules & Expectations!**\n"
                "[Terms and Conditions](https://discordapp.com/terms)\n"
                "[Privacy Policy](https://discordapp.com/privacy)\n"
                "[Guidelines](https://discordapp.com/guidelines)\n\n"
                "**Rule 1: Courteous Conduct**\n"
                "Demonstrate courtesy and consideration. Embrace diverse perspectives and opinions. Engage in debates respectfully; say no to harassment and trolling.\n\n"
                "**Rule 2: Content Standards**\n"
                "Decline repetitive messages, excessive user tagging, and harmful content. Keep NSFW content away from our realms.\n\n"
                "**Rule 3: No Spam or Advertising**\n"
                "Reject repetitive messages, excessive user tagging, and harmful materials. Direct advertising and affiliate links are unwelcome.\n\n"
                "**Rule 4: Channel Etiquette**\n"
                "Navigate channels wisely; use them as intended. Role mentions should align with the channel's theme.\n\n"
                "**Rule 5: Privacy and Personal Information**\n"
                "Safeguard personal information as a dragon guards its treasure. No doxxing, sharing addresses, phone numbers, and sensitive data."
            ),
            color=discord.Color.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1122516656837623839/1322539123503796335/bwrules.gif?ex=67713e0a&is=676fec8a&hm=b9e47f206c72ab155cee7f9eef4f57fc9b9a343a179c4034b0d6257856db3cec&")

        await channel.send(embed=embed)
        await interaction.response.send_message("Discord rules posted successfully!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(GuildInfoCog(bot))
