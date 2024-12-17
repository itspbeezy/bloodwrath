import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Bot setup with necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Constants
ATTENDANCE_CHANNEL_ID = 1316208046787133450
ABSENCE_CHANNEL_ID = 1317274570914533417
AUTHORIZED_ROLE_ID = 1288636427747459083

class AbsenceModal(discord.ui.Modal, title='Absence Report'):
    in_game_name = discord.ui.TextInput(
        label='In game name',
        placeholder='Enter your in-game name...',
        required=True,
    )
    
    events = discord.ui.TextInput(
        label='Events you will be missing',
        placeholder='List the events...',
        required=True,
    )
    
    dates = discord.ui.TextInput(
        label='Dates you will be gone',
        placeholder='Enter the dates...',
        required=True,
    )
    
    reason = discord.ui.TextInput(
        label='Reason',
        placeholder='Explain your absence...',
        style=discord.TextStyle.paragraph,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Get the absence channel
        absence_channel = interaction.guild.get_channel(ABSENCE_CHANNEL_ID)
        
        # Create embed for the absence report
        embed = discord.Embed(
            title="Absence Report",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Discord User", value=f"{interaction.user.mention} ({interaction.user.name})", inline=False)
        embed.add_field(name="In-game Name", value=self.in_game_name.value, inline=False)
        embed.add_field(name="Events Missing", value=self.events.value, inline=False)
        embed.add_field(name="Dates", value=self.dates.value, inline=False)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        
        await absence_channel.send(embed=embed)
        await interaction.response.send_message("Your absence report has been submitted.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="attendance", description="Take attendance of all users in voice channels")
@app_commands.default_permissions(administrator=True)
async def attendance(interaction: discord.Interaction):
    # Get the attendance channel
    attendance_channel = interaction.guild.get_channel(ATTENDANCE_CHANNEL_ID)
    
    # Get current time in EST
    est = pytz.timezone('US/Eastern')
    current_time = datetime.now(est)
    
    # Create embed for attendance
    embed = discord.Embed(
        title="Attendance Report",
        description=f"Taken on {current_time.strftime('%Y-%m-%d at %I:%M %p EST')}",
        color=discord.Color.green()
    )
    
    # Iterate through all voice channels
    for vc in interaction.guild.voice_channels:
        # Get members in the voice channel
        members = vc.members
        if members:
            # Create a formatted list of members
            member_list = "\n".join([f"• {member.name}" for member in members])
            embed.add_field(
                name=f"{vc.name} ({len(members)} members)",
                value=member_list,
                inline=False
            )
    
    await attendance_channel.send(embed=embed)
    await interaction.response.send_message("Attendance has been recorded.", ephemeral=True)

@bot.tree.command(name="absent", description="Submit an absence report")
async def absent(interaction: discord.Interaction):
    # Check if user has the required role
    if not any(role.id == AUTHORIZED_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message(
            "You don't have permission to use this command.",
            ephemeral=True
        )
        return
    
    # Send the modal to the user
    await interaction.response.send_modal(AbsenceModal())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')