import discord
from discord.ext import commands
from discord import app_commands

# Role and admin permission check
def has_admin_or_roles(role_ids):
    def predicate(interaction):
        """Check if the user has admin permissions or a required role."""
        if isinstance(interaction.user, discord.Member):
            is_admin = interaction.user.guild_permissions.administrator
            has_role = any(role.id in role_ids for role in interaction.user.roles)
            return is_admin or has_role
        return False
    return app_commands.check(predicate)

# Button class for user interaction
class ItemSelectionButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.bis_users = set()
        self.trait_users = set()
        self.sell_users = set()

    @discord.ui.button(label="Best In Slot (BIS)", style=discord.ButtonStyle.green, custom_id="button_bis")
    async def bis_button(self, interaction, button):
        """Handle Best In Slot (BIS) button interaction."""
        self.bis_users.add(interaction.user)
        await interaction.response.send_message("You selected **Best In Slot (BIS)**.", ephemeral=True)

    @discord.ui.button(label="Trait", style=discord.ButtonStyle.blurple, custom_id="button_trait")
    async def trait_button(self, interaction, button):
        """Handle Trait button interaction."""
        self.trait_users.add(interaction.user)
        await interaction.response.send_message("You selected **Trait**.", ephemeral=True)

    @discord.ui.button(label="Sell", style=discord.ButtonStyle.red, custom_id="button_sell")
    async def sell_button(self, interaction, button):
        """Handle Sell button interaction."""
        self.sell_users.add(interaction.user)
        await interaction.response.send_message("You selected **Sell**.", ephemeral=True)

    def get_results(self):
        """Retrieve the results for each button."""
        results = {
            "BIS": [user.display_name for user in self.bis_users],
            "Trait": [user.display_name for user in self.trait_users],
            "Sell": [user.display_name for user in self.sell_users],
        }
        return results

class ButtonTrackerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_views = {}  # Track active views per channel

    @app_commands.command(name="post_buttons", description="Post item selection buttons.")
    @has_admin_or_roles([1308283136786042970, 1308283382513274910])
    async def post_buttons(self, interaction):
        """Post the buttons to the thread or channel."""
        view = ItemSelectionButtons()
        self.active_views[interaction.channel.id] = view

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
        view = self.active_views.get(interaction.channel.id)
        if not view:
            await interaction.response.send_message("No buttons have been posted yet in this channel.", ephemeral=True)
            return

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

async def setup(bot):
    await bot.add_cog(ButtonTrackerCog(bot))