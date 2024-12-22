import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from discord import Interaction


# Permission check for admins and specific roles
def has_admin_or_roles(role_ids):
    def predicate(interaction):
        """Check if the user has admin permissions or required roles."""
        if isinstance(interaction.user, discord.Member):
            is_admin = interaction.user.guild_permissions.administrator
            has_role = any(role.id in role_ids for role in interaction.user.roles)
            return is_admin or has_role
        return False
    return app_commands.check(predicate)

# Role assignment for rolls
class ConfirmRulesView(View):
    def __init__(self, role_id):
        super().__init__(timeout=None)
        self.role_id = role_id

    @discord.ui.button(label="I Agree", style=discord.ButtonStyle.green, custom_id="confirm_rules")
    async def confirm_rules(self, interaction: Interaction, button: Button):
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

# Cog class for button tracking
class ButtonTrackerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="post_buttons", description="Post item selection buttons.")
    @has_admin_or_roles([1308283136786042970, 1308283382513274910])
    async def post_buttons(self, interaction):
        """Post the buttons for item selection."""
        # Define buttons for BIS, Trait, and Sell
        class ItemSelectionButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.bis_users = set()
                self.trait_users = set()
                self.sell_users = set()

            @discord.ui.button(label="Best In Slot (BIS)", style=discord.ButtonStyle.green, custom_id="button_bis")
            async def bis_button(self, interaction, button):
                """Handle BIS button click."""
                self.bis_users.add(interaction.user)
                await interaction.response.send_message("You selected **Best In Slot (BIS)**.", ephemeral=True)

            @discord.ui.button(label="Trait", style=discord.ButtonStyle.blurple, custom_id="button_trait")
            async def trait_button(self, interaction, button):
                """Handle Trait button click."""
                self.trait_users.add(interaction.user)
                await interaction.response.send_message("You selected **Trait**.", ephemeral=True)

            @discord.ui.button(label="Sell", style=discord.ButtonStyle.red, custom_id="button_sell")
            async def sell_button(self, interaction, button):
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

        # Instantiate the buttons view
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
    async def list_results(self, interaction):
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

    @app_commands.command(name="post_rules", description="Post the guild rules.")
    @has_admin_or_roles([1308283136786042970, 1308283382513274910])
    async def post_rules(self, interaction):
        """Post the guild rules."""
        embed = discord.Embed(
            title="Guild Rules and Loot Policies",
            description=(
                "**Guild Rules:**\n"
                "- Be friendly and helpful\n"
                "- Be active\n"
                "- Maintain a weekly guild reputation of **5000+**. Anything lower will result in warnings and removal.\n"
                "- **MANDATORY** attendance for ARCH / 8PM CONFLICT BOSSES. 11PM BOSSES ARE NOT MANDATORY.\n\n"
                "**Upcoming GvG Content (Rifts, Boons):**\n"
                "- A list of enemy healers and tanks will be sent out:\n"
                "  - **Feud the healers** to make them easier to target.\n"
                "  - **Interest the tanks** to avoid hitting them.\n"
                "- This makes destabilizing the enemy's core group easier.\n"
                "- A list of names will be provided before each war.\n\n"
                "**Loot Rules:**\n"
                "- To qualify for loot, you must have a minimum of **10,000 guild reputation**.\n"
                "- If there are minimal players at a world boss (1-6), the dropper has the following options:\n"
                "  - Sell the item directly.\n"
                "  - Offer it to the guild for others to roll as a BIS item.\n"
                "  - Transfer the item directly to a player in the party if they need it and the party agrees.\n\n"
                "**ArchBoss Drops:**\n"
                "- These items are handled by the **BloodWrath Council** based on who benefits the most.\n"
                "- Eligibility requires:\n"
                "  - Being active in the guild for at least **3 weeks**.\n"
                "  - High Discord and in-game activity.\n"
                "  - Participation in events and willingness to help grow the guild.\n"
                "- **Council Members:**\n"
                "  - <@189592972461867017>\n"
                "  - <@289221843855081472>\n"
                "  - <@170022663551451136>\n"
                "  - <@926111915657289730>\n"
                "  - <@269955781665751040>\n"
                "  - <@121386563828580352>\n"
                "  - <@133301442491449344>\n"
                "  - <@171753483467227136>\n"
                "  - <@1034290439441879062>\n"
                "  - <@284877369049743360>\n"
                "- Selection Process:\n"
                "  - Each council member nominates **3 users** who meet the criteria.\n"
                "  - The user with the **most votes** receives the item.\n"
                "  - In case of a tie, a roll is used to decide."
            ),
            color=discord.Color.red()
        )

        await interaction.response.send_message(embed=embed)

# Command to post the rules with the button
@app_commands.command(name="post_rolling_rules", description="Post the rolling rules with the acknowledgment button.")
@has_admin_or_roles([1308283136786042970, 1308283382513274910])
async def post_rolling_rules(self, interaction):
    """Post the rolling rules and provide a button for acknowledgment."""
    role_id = 1296641442164379678  # Replace with the actual role ID for "Item Rolls"
    view = ConfirmRulesView(role_id)

    embed = discord.Embed(
        title="Rolling Rules",
        description=(
            "**Please read and acknowledge the following rules:**\n\n"
            "**1. Item Roll Posts:**\n"
            "- Include a **screenshot** of the desired item.\n"
            "- The title must contain the **item name** and **trait**.\n"
            "- Failure to follow these rules will result in deletion of your post.\n\n"
            "**2. Contest Period:**\n"
            "- Posts remain open for **24 hours**.\n"
            "- After 24 hours, the reward goes to the **highest roller**.\n\n"
            "**3. Rolling Process:**\n"
            "- Rolls use a **D100** system.\n"
            "- Only the **first roll** is valid.\n\n"
            "**4. User Responsibility:**\n"
            "- You are responsible for checking guild loot and forum posts.\n"
            "- No one will create posts on your behalf.\n\n"
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

async def setup(bot):
    await bot.add_cog(ButtonTrackerCog(bot))