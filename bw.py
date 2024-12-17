import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup with necessary intents
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Constants
ATTENDANCE_CHANNEL_ID = 1316208046787133450
ABSENCE_CHANNEL_ID = 1317274570914533417
AUTHORIZED_ROLE_ID = 1288636427747459083

class AbsenceModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="In game name",
                placeholder="Enter your in-game name...",
                custom_id="in_game_name",
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Events you will be missing",
                placeholder="List the events...",
                custom_id="events",
                max_length=100,
            ),
            disnake.ui.TextInput(
                label="Dates you will be gone",
                placeholder="Enter the dates...",
                custom_id="dates",
                max_length=100,
            ),
            disnake.ui.TextInput(
                label="Reason",
                placeholder="Explain your absence...",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                max_length=1000,
            ),
        ]
        super().__init__(title="Absence Report", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        # Get the absence channel
        absence_channel = inter.guild.get_channel(ABSENCE_CHANNEL_ID)
        
        # Create embed for the absence report
        embed = disnake.Embed(
            title="Absence Report",
            color=disnake.Color.blue(),
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Discord User", value=f"{inter.user.mention} ({inter.user.name})", inline=False)
        embed.add_field(name="In-game Name", value=inter.text_values["in_game_name"], inline=False)
        embed.add_field(name="Events Missing", value=inter.text_values["events"], inline=False)
        embed.add_field(name="Dates", value=inter.text_values["dates"], inline=False)
        embed.add_field(name="Reason", value=inter.text_values["reason"], inline=False)
        
        await absence_channel.send(embed=embed)
        await inter.response.send_message("Your absence report has been submitted.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        print('Syncing commands...')
        await bot.sync_commands()
        print('Commands synced successfully!')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.slash_command(name="attendance", description="Take attendance of all users in voice channels")
@commands.has_permissions(administrator=True)
async def attendance(inter: disnake.ApplicationCommandInteraction):
    # Get the attendance channel
    attendance_channel = inter.guild.get_channel(ATTENDANCE_CHANNEL_ID)
    
    # Get current time in EST
    est = pytz.timezone('US/Eastern')
    current_time = datetime.now(est)
    
    # Create embed for attendance
    embed = disnake.Embed(
        title="Attendance Report",
        description=f"Taken on {current_time.strftime('%Y-%m-%d at %I:%M %p EST')}",
        color=disnake.Color.green()
    )
    
    # Iterate through all voice channels
    for vc in inter.guild.voice_channels:
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
    await inter.response.send_message("Attendance has been recorded.", ephemeral=True)

@bot.slash_command(name="absent", description="Submit an absence report")
async def absent(inter: disnake.ApplicationCommandInteraction):
    # Check if user has the required role
    if not any(role.id == AUTHORIZED_ROLE_ID for role in inter.user.roles):
        await inter.response.send_message(
            "You don't have permission to use this command.",
            ephemeral=True
        )
        return
    
    # Send the modal to the user
    await inter.response.send_modal(modal=AbsenceModal())

# Bot token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)