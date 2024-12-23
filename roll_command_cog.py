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
        class RollModal(discord.ui.Modal, title="Item Roll Form"):
            def __init__(self):
                super().__init__()

                self.add_item(discord.ui.TextInput(
                    label="Do you have the required Guild Reputation (10k GREP)?",
                    placeholder="Yes or No",
                    required=True,
                    max_length=3
                ))

                self.add_item(discord.ui.TextInput(
                    label="Select the type of item",
                    placeholder="Options: PVP BIS, PVE BIS, Trait, Sell, Lithograph",
                    required=True
                ))

            async def on_submit(self, modal_interaction: discord.Interaction):
                # Retrieve user input
                guild_rep = self.children[0].value.strip().lower()
                item_type = self.children[1].value.strip().lower()

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
        await interaction.response.send_modal(RollModal())

async def setup(bot: commands.Bot):
    await bot.add_cog(RollCommandCog(bot))
