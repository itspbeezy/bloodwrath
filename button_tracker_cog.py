import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

# Permission check for admins and specific roles
def has_admin_or_roles(role_ids):
    def predicate(interaction: discord.Interaction):
        """Check if the user has admin permissions or required roles."""
        if isinstance(interaction.user, discord.Member):
            is_admin = interaction.user.guild_permissions.administrator
            has_role = any(role.id in role_ids for role in interaction.user.roles)
            return is_admin or has_role
        return False
    return app_commands.check(predicate)

# View for the acknowledgment button
class ConfirmRulesView(View):
    def __init__(self, role_id: int):
        super().__init__(timeout=None)
        self.role_id = role_id

    @discord.ui.button(label="I Agree", style=discord.ButtonStyle.green, custom_id="confirm_rules")
    async def confirm_rules(self, interaction: discord.Interaction, button: Button):
        """Assign the role to the user when they click the button."""
        guild = interaction.guild
        member = interaction.user
        role = guild.get_role(self.role_id)

        if role in member.roles:
            await interaction.response.send_message(
                "You already have the required role.", ephemeral=True
            )
        else:
            await member.add_roles(role)
            await interaction.response.send_message(
                "You have been assigned the **Item Rolls** role. Thank you for confirming!",
                ephemeral=True,
            )

# View for item selection buttons
class ItemSelectionButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.bis_users = set()
        self.trait_users = set()
        self.sell_users = set()

    @discord.ui.button(label="Best In Slot (BIS)", style=discord.ButtonStyle.green, custom_id="button_bis")
    async def bis_button(self, interaction: discord.Interaction, button: Button):
        """Handle BIS button click."""
        self.bis_users.add(interaction.user)
        await interaction.response.send_message("You selected **Best In Slot (BIS)**.", ephemeral=True)

    @discord.ui.button(label="Trait", style=discord.ButtonStyle.blurple, custom_id="button_trait")
    async def trait_button(self, interaction: discord.Interaction, button: Button):
        """Handle Trait button click."""
        self.trait_users.add(interaction.user)
        await interaction.response.send_message("You selected **Trait**.", ephemeral=True)

    @discord.ui.button(label="Sell", style=discord.ButtonStyle.red, custom_id="button_sell")
    async def sell_button(self, interaction: discord.Interaction, button: Button):
        """Handle Sell button click."""
        self.sell_users.add(interaction.user)
        await interaction.response.send_message("You selected **Sell**.", ephemeral=True)

    def get_results(self):
        """Retrieve the results for each button."""
        return {
            "BIS": [user.display_name for user in self.bis_users],
            "Trait": [user.display_name for user in self.trait_users],
            "Sell": [user.display_name for user in self.sell_users],
        }

# Cog class for button tracking
class ButtonTrackerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="post_buttons", description="Post item selection buttons.")
    @has_admin_or_roles([1308283136786042970, 1308283382513274910])
    async def post_buttons(self, interaction: discord.Interaction):
        """Post the buttons for item selection."""
        view = ItemSelectionButtons()

        embed = discord.Embed(
            title="Item Selection",
            description=(
                "**Please select a button depending on your needs.**\n"
                "Best in slot rollers will always have priority over trait and sales. "
                "You will need to submit proof if this is a best in slot item, such as a screenshot "
                "of your current gear and build link you are following."
            ),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="list_results", description="List users who selected each button.")
    @has_admin_or_roles([1308283136786042970, 1308283382513274910])
    async def list_results(self, interaction: discord.Interaction):
        """List the users who selected each button."""
        view = ItemSelectionButtons()
        results = view.get_results()

        embed = discord.Embed(
            title="Item Selection Results",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Best In Slot (BIS)",
            value="\n".join(results["BIS"]) if results["BIS"] else "No users selected.",
            inline=False
        )
        embed.add_field(
            name="Trait",
            value="\n".join(results["Trait"]) if results["Trait"] else "No users selected.",
            inline=False
        )
        embed.add_field(
            name="Sell",
            value="\n".join(results["Sell"]) if results["Sell"] else "No users selected.",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="post_rolling_rules", description="Post the rolling rules with the acknowledgment button.")
    @has_admin_or_roles([1308283136786042970, 1308283382513274910])
    async def post_rolling_rules(self, interaction: discord.Interaction):
        """Post the rolling rules and provide a button for acknowledgment."""
        role_id = 1296641442164379678  # Replace with the actual role ID for "Item Rolls"
        view = ConfirmRulesView(role_id)

        embed = discord.Embed(
            title="Rolling Rules",
            description=(
                "**Please read and acknowledge the following rules:**\n\n"
                "**1. Item Roll Posts:**\n"
                "- Staff will post the item in the loot-rolling channel.\n"
                "- If you want the item you must roll for the item on TLGM app.\n"
                "- You must have a screenshot of your gear and updated builds on TLGM app.\n\n"
                "**2. Contest Period:**\n"
                "- Posts remain open until loot days on Tuesdays and Saturdays.\n"
                "- On those days, the reward goes to the **highest roller**.\n\n"
                "**3. Rolling Process:**\n"
                "- Rolls use a **D100** system.\n"
                "- All roles are handled via TLGM.\n\n"
                "**4. User Responsibility:**\n"
                "- You are responsible for checking guild loot and forum posts.\n"
                "- No one will alert you on these posts.\n\n"
                "**5. Intended Use:**\n"
                "- Include the **intended use** for the item in your post.\n"
                "- Abuse or dishonesty will result in **penalties**.\n\n"
                "**6. Acknowledge and Agree:**\n"
                "- React below or click the button to confirm.\n"
                "- You will be assigned the **Item Rolls** role upon acknowledgment."
            ),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="post_loot_policy", description="Post the loot policy to the designated channel.")
    async def post_loot_policy(self, interaction: discord.Interaction):
        """Command to post the loot policy."""
        channel_id = 1235798906382585909  # Replace with the actual channel ID
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            await interaction.response.send_message("The designated channel could not be found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Archboss Drops & Expectations",
            description=(
                "**Loot System:**\n\n"
                "For Archboss drops, a loot council system is in place, as outlined by Blood Wrath Leadership. "
                "This ensures these powerful weapons remain within Blood Wrath and out of enemy hands. "
                "The council votes on the most suitable member to receive the item, with the nominee receiving "
                "the most votes awarded the weapon.\n\n"
                "In the event of a tie, one of two resolutions will occur:\n"
                "1. The tied members may roll for the item.\n"
                "2. Luchii will make the final decision.\n\n"
                "Luchii will always have the final decision as there are special circumstances that not all of the council are aware of.\n\n"
                "Arch Boss Weapons are only considered for GVG builds.\n\n"

                "**Archboss Expectations:**\n\n"
                "To qualify for Archboss drops, members must meet the following criteria:\n"
                "- Proper weapon utilization\n"
                "- Significant guild contributions (Guild Rep/Activity)\n"
                "- Individual player skills\n"
                "- Consistency in performance\n"
                "- Strong static play\n\n"

                "**Weapon Guidelines**\n"
                "**Queen Bellandir’s Weapons**\n\n"
                "**Languishing Blade:**\n"
                "- Frontline hard engage\n"
                "- Large group positioning\n"
                "- Mastery of Annihilating Slash\n"
                "- Survivability\n"
                "- Consistent performance in GvG/ZvZ\n\n"

                "**Hivemind Staff:**\n"
                "- High kill ranking\n"
                "- Effective use of Fire skills\n"
                "- Consistent performance in GvG/ZvZ\n\n"

                "**Toxic Spine Throwers:**\n"
                "- Mastery of single-target tank shred or bombing disruptions\n"
                "- Significant impact in fights\n"
                "- Consistent performance in GvG/ZvZ\n\n"

                "**Serrated Spike:**\n"
                "- Expertise in spear play\n"
                "- Skilled in ball disruptions or guild setups\n"
                "- Consistent performance in GvG/ZvZ\n\n"

                "**Tevent’s Weapons**\n\n"
                "**Warblade of Despair:**\n"
                "- Identifying high-priority targets\n"
                "- High DPS\n"
                "- Strength in 1v1 situations\n"
                "- Effective in large-group engagements\n"
                "- Consistent performance in GvG/ZvZ\n\n"

                "**Fangs of Fury:**\n"
                "- High single-target damage\n"
                "- Proficient in camouflage skills\n"
                "- Strong 1v1 abilities\n"
                "- Adept at locating high-priority targets\n\n"

                "**Arc of Wailing Death:**\n"
                "- Locating high-priority targets\n"
                "- High DPS output\n"
                "- Proficiency in 1v1 encounters\n"
                "- Consistent performance in GvG/ZvZ\n\n"

                "**Grasp of Withering:**\n"
                "- Targeting high-priority enemies\n"
                "- High DPS\n"
                "- Accurate positioning for large-area sleeps\n"
                "- Capability to eliminate tanks\n"
                "- Strong in 1v1 scenarios\n"
                "- Consistent performance in GvG/ZvZ\n\n"

                "**Questions or Concerns**\n\n"
                "For further inquiries, please ask in the <#1323922651105984575> channel."
            ),
            color=discord.Color.gold()
        )

        await channel.send(embed=embed)
        await interaction.response.send_message("Loot policy posted successfully!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ButtonTrackerCog(bot))