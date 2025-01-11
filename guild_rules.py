import discord
from discord.ext import commands
from discord import app_commands

class GuildRulesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="guild_rules", description="Post the guild rules and loot policies.")
    @app_commands.checks.has_any_role(1215718493622894603, 1308283136786042970)
    async def guild_rules(self, interaction: discord.Interaction):
        """Post the guild rules and loot policies in the designated channel."""
        channel_id = 1320523622116495430  # Guild rules channel
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            await interaction.response.send_message("Could not find the guild rules channel.", ephemeral=True)
            return

        embed = discord.Embed(title="Guild Rules and Loot Policies", color=discord.Color.red())
        embed.add_field(name="Guild Rules:", value=(
            "- Be friendly and helpful\n"
            "- Be active\n"
            "- Maintain a weekly guild reputation of 5000+. Anything lower will result in warnings and removal.\n"
            "- **MANDATORY attendance for ARCH BOSSES.**"
        ), inline=False)
        
        embed.add_field(name="Upcoming GvG Content (Rifts, Boons):", value=(
            "- A list of enemy healers and tanks will be sent out.\n"
            "- Feud the healers to make them easier to target.\n"
            "- Interest the tanks to avoid hitting them.\n"
            "- This makes destabilizing the enemy's core group easier.\n"
            "- A list of names will be provided before each war."
        ), inline=False)
        
        embed.add_field(name="Loot Rules:", value=(
            "- To qualify for loot, you must have a minimum of 10,000 guild reputation.\n"
            "- If there are minimal players at a world boss (1-3), the dropper has the following options:\n"
            "  - Sell the item directly.\n"
            "  - Offer it to the guild for others to roll as a BIS item.\n"
            "  - Transfer the item directly to a player in the party if they need it and the party agrees."
        ), inline=False)
        
        embed.add_field(name="Loot Distribution:", value=(
            "- For **Fire**, loot will always be posted in: <#1323505958348918854>\n"
            "- For **Water**, loot will always be posted in: <#1324564030261825600>\n"
            "- Loot will be handed out on **Wednesdays and Saturdays**\n"
            "- **Priority order:** PVP BIS > PVE BIS > TRAIT > SELLING > LITHOGRAPH"
        ), inline=False)
        
        embed.add_field(name="Eligibility Requirements:", value=(
            "- You must sign up and join us on TLGM to be eligible to roll for loot: [Join TLGM](https://tlgm.app/guilds/join/character?guild_id=Ub-gzVHMUeq7fLxt6pTme)\n"
            "- Players that make required events (boons, rifts, archs) receive an additional **1000 guild rep**.\n"
            "- You must attend events.\n"
            "  - Fire events: <#1325596268973523116>\n"
            "  - Water events: <#1324565142180073665>"
        ), inline=False)
        
        embed.add_field(name="Alliance Discord:", value=(
            "Join our alliance Discord and request roles: [Alliance Discord](https://discord.gg/sev7wcPVNa)\n"
            "You must change your nickname in the server to the following format: **(BW) Name**"
        ), inline=False)
        
        embed.add_field(name="Questions:", value=(
            "If you have any questions, please feel free to ask here: <#1323922651105984575>"
        ), inline=False)

        await channel.send(embed=embed)
        await interaction.response.send_message("Guild rules and loot policies have been posted successfully.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(GuildRulesCog(bot))
