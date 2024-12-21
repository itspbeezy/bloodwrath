import discord
from discord.ext import commands
from discord import app_commands

# Role and admin permission check
def has_admin_or_roles(role_ids):
    def predicate(interaction: discord.Interaction):
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
    async def bis_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bis_users.add(interaction.user)
        await interaction.response.send_message("You selected **Best In Slot (BIS)**.", ephemeral=True)

    @discord.ui.button(label="Trait", style=discord.ButtonStyle.blurple, custom_id="button_trait")
    async def trait_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.trait_users.add(interaction.user)
        await interaction.response.send_message("You selected **Trait**.", ephemeral=True)

    @discord.ui.button(label="Sell", style=discord.ButtonStyle.red, custom_id="button_sell")
    async def sell_button(self, interaction: discord.Interaction, button: discord.ui.Button):
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
    async def post_buttons(self, interaction: discord.Interaction):
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
    async def list_results(self, interaction: discord.Interaction):
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
    async def post_rules(self, interaction: discord.Interaction):
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
                "A list of enemy healers and tanks will be sent out:\n"
                "- Feud the healers to target them.\n"
                "- Interest the tanks to avoid hitting them.\n"
                "This makes destabilizing the enemy's ball easier.\n"
                "Before each war, a list of names will be provided for targeting.\n\n"
                "**Loot Rules:**\n"
                "- To qualify for loot, you must have a minimum of **10,000 guild reputation**.\n"
                "- The council will post loot details in <#1295194850584432710>, including the item name, trait, and screenshot.\n"
                "- Use the bot's buttons (Best In Slot, Trait, Sell) to indicate your need:\n"
                "  - **BIS:** You NEED the item for your build.\n"
                "  - **Trait:** You need the trait.\n"
                "  - **Sell:** You want the item for Lucent.\n\n"
                "**ArchBoss Drops:**\n"
                "- Handled by the council, based on who benefits the most.\n"
                "- Multiple candidates will roll for it, or the item will be sold for guild-wide benefits.\n"
                "- These rules may evolve as BloodWrath grows and learns together."
            ),
            color=discord.Color.red()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ButtonTrackerCog(bot))