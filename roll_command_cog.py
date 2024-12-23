import discord
from discord.ext import commands
from discord import app_commands
import random

class RollCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Roll for an item with guild requirements.")
    async def roll(self, interaction: discord.Interaction):
        """Command to roll for an item."""

        # First question: Guild Reputation check
        async def ask_guild_reputation():
            options = [
                discord.SelectOption(label="Yes", description="I have the required Guild Reputation (10k GREP).", value="yes"),
                discord.SelectOption(label="No", description="I do not meet the Guild Reputation requirements.", value="no")
            ]

            select = discord.ui.Select(placeholder="Do you have the required Guild Reputation (10k GREP)?", options=options)

            async def select_callback(interaction: discord.Interaction):
                if select.values[0] == "yes":
                    await ask_item_type()
                else:
                    await interaction.response.send_message(
                        "You do not meet the minimum requirements to roll for this item. Get to work and get that rep up young blood!",
                        ephemeral=True
                    )

            select.callback = select_callback

            view = discord.ui.View()
            view.add_item(select)
            await interaction.response.send_message(view=view, ephemeral=True)

        # Second question: Item type selection
        async def ask_item_type():
            options = [
                discord.SelectOption(label="PVP BIS (Priority)", description="Roll for a PVP BIS item.", value="pvp_bis"),
                discord.SelectOption(label="PVE BIS", description="Roll for a PVE BIS item.", value="pve_bis"),
                discord.SelectOption(label="Trait", description="Roll for a trait item.", value="trait"),
                discord.SelectOption(label="Sell", description="Roll for a sellable item.", value="sell"),
                discord.SelectOption(label="Lithograph", description="Roll for a lithograph item.", value="lithograph")
            ]

            select = discord.ui.Select(placeholder="Please select the following for this item:", options=options)

            async def select_callback(interaction: discord.Interaction):
                selected_option = select.values[0]
                roll_result = random.randint(0, 100)

                # Map selected option to user-friendly label
                option_map = {
                    "pvp_bis": "PVP BIS (Priority)",
                    "pve_bis": "PVE BIS",
                    "trait": "Trait",
                    "sell": "Sell",
                    "lithograph": "Lithograph"
                }
                readable_option = option_map[selected_option]

                embed = discord.Embed(
                    title="Roll Results",
                    description=(
                        f"**Meets Guild Reputation:** Yes\n"
                        f"**Selected Option:** {readable_option}\n"
                        f"**Dice Roll:** {roll_result}"
                    ),
                    color=discord.Color.green()
                )

                await interaction.response.send_message(embed=embed, ephemeral=True)

            select.callback = select_callback

            view = discord.ui.View()
            view.add_item(select)
            await interaction.followup.send(view=view, ephemeral=True)

        # Start the interaction with the guild reputation question
        await ask_guild_reputation()

async def setup(bot: commands.Bot):
    await bot.add_cog(RollCommandCog(bot))
