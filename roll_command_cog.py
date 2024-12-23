import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class RollCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Roll for an item with guild requirements.")
    async def roll(self, interaction: discord.Interaction):
        """Command to roll for an item."""
        # Defer the interaction to prevent timeout
        await interaction.response.defer(ephemeral=False)

        class RollModal(discord.ui.Modal, title="Item Roll Form"):
            def __init__(self):
                super().__init__()

                self.guild_rep_input = discord.ui.TextInput(
                    label="Do you have the required Guild Reputation (10k GREP)?",
                    placeholder="Yes or No",
                    required=True,
                    max_length=3
                )
                self.add_item(self.guild_rep_input)

                self.item_type_input = discord.ui.TextInput(
                    label="Select the type of item",
                    placeholder="Options: PVP BIS, PVE BIS, Trait, Sell, Lithograph",
                    required=True
                )
                self.add_item(self.item_type_input)

            async def on_submit(self, modal_interaction: discord.Interaction):
                guild_rep = self.guild_rep_input.value.strip().lower()
                item_type = self.item_type_input.value.strip().lower()

                if guild_rep != "yes":
                    await modal_interaction.response.send_message(
                        "You do not meet the minimum requirements to roll for this item. Get to work and get that rep up young blood!",
                        ephemeral=True
                    )
                    return

                valid_options = ["pvp bis", "pve bis", "trait", "sell", "lithograph"]
                if item_type not in valid_options:
                    await modal_interaction.response.send_message(
                        "Invalid item type selected. Please try again.", ephemeral=True
                    )
                    return

                # Simulate dice roll
                dice_message = await modal_interaction.response.send_message(
                    f"{interaction.user.mention} is rolling the dice... 🎲", ephemeral=False
                )

                for _ in range(3):
                    await asyncio.sleep(1)
                    await dice_message.edit(content=f"🎲 Rolling... {random.randint(1, 100)}")

                final_roll = random.randint(1, 100)
                readable_option = item_type.upper()

                # Display results
                embed = discord.Embed(
                    title="Roll Results",
                    description=(
                        f"**User:** {interaction.user.mention}\n"
                        f"**Meets Guild Reputation:** Yes\n"
                        f"**Selected Option:** {readable_option}\n"
                        f"**Dice Roll:** {final_roll}"
                    ),
                    color=discord.Color.green()
                )
                await dice_message.edit(content=f"{interaction.user.mention}'s roll is complete! 🎲", embed=embed)

        # Send modal
        await interaction.followup.send_modal(RollModal())

async def setup(bot: commands.Bot):
    await bot.add_cog(RollCommandCog(bot))