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
        # Embed for modal header
        embed = discord.Embed(
            title="Guild Reputation Check",
            description="Do you have the required Guild Reputation (10k GREP)?",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1288633288717766706/1320526678337785951/discordserverlogo4.gif?ex=676a948e&is=6769430e&hm=ce36711dd71669279694b55cd999c6ee7ce75299660c61c89e3f26e1c4654dcb&")

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Modal for Guild Reputation Check
        class GuildReputationModal(discord.ui.Modal, title="Guild Reputation Check"):
            def __init__(self):
                super().__init__()
                self.answer = discord.ui.TextInput(
                    label="Do you have the required Guild Reputation (10k GREP)?",
                    placeholder="Yes or No",
                    required=True
                )
                self.add_item(self.answer)

            async def on_submit(self, modal_interaction: discord.Interaction):
                if self.answer.value.strip().lower() != "yes":
                    await modal_interaction.response.send_message(
                        "You do not meet the minimum requirements to roll for this item. Get to work and get that rep up young blood!",
                        ephemeral=True
                    )
                else:
                    await ask_item_type(modal_interaction)

        # Modal for Item Type Selection
        class ItemTypeModal(discord.ui.Modal, title="Item Selection"):
            def __init__(self):
                super().__init__()
                self.item_type = discord.ui.TextInput(
                    label="Please select the type of item:",
                    placeholder="Options: PVP BIS, PVE BIS, Trait, Sell, Lithograph",
                    required=True
                )
                self.add_item(self.item_type)

            async def on_submit(self, modal_interaction: discord.Interaction):
                valid_options = ["pvp bis", "pve bis", "trait", "sell", "lithograph"]
                selected_option = self.item_type.value.strip().lower()

                if selected_option not in valid_options:
                    await modal_interaction.response.send_message(
                        "Invalid selection. Please try again.", ephemeral=True
                    )
                else:
                    await show_dice_roll(modal_interaction, selected_option)

        async def ask_guild_reputation():
            modal = GuildReputationModal()
            await interaction.followup.send_modal(modal)

        async def ask_item_type(previous_interaction: discord.Interaction):
            modal = ItemTypeModal()
            await previous_interaction.response.send_modal(modal)

        async def show_dice_roll(previous_interaction: discord.Interaction, selected_option):
            dice_message = await previous_interaction.followup.send(
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

        # Start the interaction flow
        await ask_guild_reputation()

async def setup(bot: commands.Bot):
    await bot.add_cog(RollCommandCog(bot))
