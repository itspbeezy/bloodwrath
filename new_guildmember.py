import discord
from discord.ext import commands
from discord import app_commands

class NewGuildMemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ginvite", description="Invite a new user to Blood Wrath.")
    @app_commands.checks.has_any_role(1215718493622894603, 1308283136786042970)
    async def ginvite(self, interaction: discord.Interaction, user: discord.Member):
        """Invite a new guild member."""
        await interaction.response.defer(ephemeral=True)  # Acknowledge the interaction

        # Role to assign
        role_id = 1288636427747459083
        role = interaction.guild.get_role(role_id)

        if not role:
            await interaction.followup.send("The role could not be found.", ephemeral=True)
            return

        # Add the role to the user
        try:
            await user.add_roles(role)
        except discord.Forbidden:
            await interaction.followup.send(
                f"I do not have permission to assign roles. Please check my permissions.", ephemeral=True
            )
            return
        except Exception as e:
            await interaction.followup.send(
                f"An error occurred while assigning the role: {e}", ephemeral=True
            )
            return

        # Send a DM to the user
        dm_message = (
            f"Welcome {user.mention} and congratulations on being accepted to **Blood Wrath**! "
            "We hope you are as excited as we are to have you in our ranks. With that said, "
            "I'm sending you this message to help you get started.\n\n"
            "You have been granted the **Blood** role, which allows you access to our members-only channels. "
            "Introduce yourself and say hi in our Guild Chat channel (<#1288633288717766706>). "
            "Also, please ensure your server nickname matches your in-game name for clarity.\n\n"
            "**Getting Started:**\n"
            "1. Create an account on our required TLGM app. Login and link to Discord; this is needed to sign up "
            "for scheduled events and roll on gear. You can do so by visiting: "
            "[Join TLGM](https://tlgm.app/guilds/join/character?guild_id=Ub-gzVHMUeq7fLxt6pTme).\n"
            "2. Select your weapons, upload a picture of your current gear, and feel free to link any builds or skill builds "
            "you may be using on your profile.\n\n"
            "**Important Channels:**\n"
            "- **Daily Posts:** (<#1288633941489618975>) Important information is posted here daily, including event registrations. "
            "Keep this channel unmuted.\n"
            "- **Attendance:** (<#1324502828932272128>) All event posts will be sent to this channel (mandatory and optional). "
            "Keep this channel unmuted.\n"
            "You must select if you are attending, not able to attend, or tentative for each event.\n"
            "- **Guild Rules:** (<#1320523622116495430>) Familiarize yourself with our rules and loot policy.\n"
            "- **Schedule:** (<#1308289712670248970>) The guild schedule is located here. This is where you can see our weekly schedule.\n"
            "- **Guild Loot:** (<#1323505958348918854>) Loot the guild acquires from peaceful and friendly bosses will be posted here. "
            "You can roll for it.\n\n"
            "If you have any questions or concerns, you can reach out to a council member or feel free to ask in Guild Questions (<#1323922651105984575>)."
        )

        try:
            await user.send(dm_message)
        except discord.Forbidden:
            await interaction.followup.send(
                f"I couldn't send a DM to {user.mention}. Please check their privacy settings or reach out to leadership for details.",
                ephemeral=True,
            )
            return

        # Post a welcome message in the channel
        try:
            await interaction.channel.send(
                f"Welcome {user.mention} to **Blood Wrath**! You have been granted the Blood role. "
                f"Introduce yourself in <#1288633288717766706> and get started!"
            )
            await interaction.followup.send(f"Welcome message sent for {user.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                f"An error occurred while sending the welcome message: {e}", ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(NewGuildMemberCog(bot))