import discord
from discord.ext import commands
from discord import app_commands

# Role and admin permission check
def has_admin_or_role(role_id):
    def predicate(interaction: discord.Interaction):
        if isinstance(interaction.user, discord.Member):
            is_admin = interaction.user.guild_permissions.administrator
            has_role = any(role.id == role_id for role in interaction.user.roles)
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
    @has_admin_or_role(1308283136786042970)
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
    @has_admin_or_role(1308283136786042970)
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

async def setup(bot):
    await bot.add_cog(ButtonTrackerCog(bot))