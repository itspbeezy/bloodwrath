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
        await interaction.response.defer()

        # First question: Guild Reputation check
        modal = discord.ui.Modal(title="Guild Reputation Check")

        class GuildReputationInput(discord.ui.TextInput):
            def __init__(self):
                super().__init__(
                    label="Do you have the required Guild Reputation (10k GREP)?",
                    placeholder="Yes or No",
                    required=True,
                )

        guild_rep_input = GuildReputationInput()
        modal.add_item(guild_rep_input)

        async def modal_callback(modal_interaction: discord.Interaction):
            answer = guild_rep_input.value.strip().lower()
            if answer != "yes":
                await interaction.followup.send(
                    f"{interaction.user.mention}, you do not meet the minimum requirements to roll for this item. Get to work and get that rep up young blood!"
                )
                return
            await ask_item_type(interaction)

        modal.on_submit = modal_callback
        await interaction.response.send_modal(modal)

        # Second question: Item type selection
        async def ask_item_type(previous_interaction: discord.Interaction):
            modal = discord.ui.Modal(title="Item Selection")

            class ItemTypeInput(discord.ui.TextInput):
                def __init__(self):
                    super().__init__(
                        label="Please select the type of item:",
                        placeholder="Options: PVP BIS, PVE BIS, Trait, Sell, Lithograph",
                        required=True,
                    )

            item_type_input = ItemTypeInput()
            modal.add_item(item_type_input)

            async def modal_callback(modal_interaction: discord.Interaction):
                selected_option = item_type_input.value.strip().lower()
                valid_options = ["pvp bis", "pve bis", "trait", "sell", "lithograph"]

                if selected_option not in valid_options:
                    await interaction.followup.send(
                        f"{interaction.user.mention}, invalid selection. Please try again."
                    )
                    return
                await show_dice_roll(interaction, selected_option)

            modal.on_submit = modal_callback
            await interaction.response.send_modal(modal)

        # Show dice roll animation and results
        async def show_dice_roll(previous_interaction: discord.Interaction, selected_option):
            dice_message = await interaction.followup.send(
                f"{interaction.user.mention} is rolling the dice..."
            )

            # Simulate dice rolling animation
            for _ in range(3):
                await asyncio.sleep(1)
                await dice_message.edit(content=f"🎲 Rolling... {random.randint(1, 100)}")

            # Final dice result
            final_roll = random.randint(1, 100)
            readable_option = selected_option.upper()

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

async def setup(bot: commands.Bot):
    await bot.add_cog(RollCommandCog(bot))
