import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class VoiceActivity:
    join_time: datetime
    leave_time: Optional[datetime] = None
    
class ActivityTracker:
    def __init__(self, start_time: datetime):
        self.start_time = start_time
        self.channel_id: int = None
        self.member_activities: Dict[int, List[VoiceActivity]] = {}
        
    def add_activity(self, member_id: int, join_time: datetime):
        if member_id not in self.member_activities:
            self.member_activities[member_id] = []
        self.member_activities[member_id].append(VoiceActivity(join_time=join_time))
        
    def record_leave(self, member_id: int, leave_time: datetime):
        if member_id in self.member_activities and self.member_activities[member_id]:
            current_session = self.member_activities[member_id][-1]
            if current_session.leave_time is None:
                current_session.leave_time = leave_time
                
    def get_total_duration(self, member_id: int) -> timedelta:
        total_duration = timedelta()
        if member_id in self.member_activities:
            for activity in self.member_activities[member_id]:
                leave_time = activity.leave_time or datetime.now(pytz.UTC)
                total_duration += leave_time - activity.join_time
        return total_duration

# Load environment variables
load_dotenv()

# Bot setup with necessary intents
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(
    command_prefix='/',
    intents=intents,
    test_guilds=[1210689535269408828]  # Replace with your server ID
)

# Constants
ATTENDANCE_CHANNEL_ID = 1316208046787133450
ABSENCE_CHANNEL_ID = 1317274570914533417
AUTHORIZED_ROLE_ID = 1288636427747459083

# Dictionary to store active monitoring sessions
active_monitors: Dict[int, ActivityTracker] = {}

[Previous AbsenceModal class remains unchanged...]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        print('Syncing commands...')
        await bot.sync_all_commands()  # Changed from sync_commands() to sync_all_commands()
        print('Commands synced successfully!')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.event
async def on_voice_state_update(member, before, after):
    guild_id = member.guild.id
    if guild_id in active_monitors:
        tracker = active_monitors[guild_id]
        
        # Record join
        if before.channel is None and after.channel and after.channel.id == tracker.channel_id:
            tracker.add_activity(member.id, datetime.now(pytz.UTC))
            
        # Record leave
        elif before.channel and before.channel.id == tracker.channel_id and \
             (after.channel is None or after.channel.id != tracker.channel_id):
            tracker.record_leave(member.id, datetime.now(pytz.UTC))

[Previous attendance command remains unchanged...]

@bot.slash_command(name="monitor", description="Start monitoring a voice channel for activity")
@commands.has_permissions(administrator=True)
async def monitor(
    inter: disnake.ApplicationCommandInteraction,
    channel: disnake.VoiceChannel = commands.Param(description="The voice channel to monitor")
):
    guild_id = inter.guild.id
    
    # Create new activity tracker
    tracker = ActivityTracker(start_time=datetime.now(pytz.UTC))
    tracker.channel_id = channel.id
    active_monitors[guild_id] = tracker
    
    # Record initial members in the channel
    for member in channel.members:
        tracker.add_activity(member.id, datetime.now(pytz.UTC))
    
    await inter.response.send_message(
        f"Now monitoring voice activity in {channel.name}. Use `/stopmonitor` to get the activity report.",
        ephemeral=True
    )

@bot.slash_command(name="stopmonitor", description="Stop monitoring and show activity report")
@commands.has_permissions(administrator=True)
async def stopmonitor(inter: disnake.ApplicationCommandInteraction):
    guild_id = inter.guild.id
    if guild_id not in active_monitors:
        await inter.response.send_message("No active monitoring session found.", ephemeral=True)
        return
        
    tracker = active_monitors[guild_id]
    channel = inter.guild.get_channel(tracker.channel_id)
    attendance_channel = inter.guild.get_channel(ATTENDANCE_CHANNEL_ID)
    
    # Record final leave time for anyone still in the channel
    current_time = datetime.now(pytz.UTC)
    for member in channel.members:
        tracker.record_leave(member.id, current_time)
    
    # Create activity report
    est = pytz.timezone('US/Eastern')
    embed = disnake.Embed(
        title="Voice Channel Activity Report",
        description=f"Channel: {channel.name}\n"
                   f"Start Time: {tracker.start_time.astimezone(est).strftime('%Y-%m-%d at %I:%M %p EST')}\n"
                   f"End Time: {current_time.astimezone(est).strftime('%Y-%m-%d at %I:%M %p EST')}",
        color=disnake.Color.blue()
    )
    
    # Sort members by total duration
    member_durations = []
    for member_id, activities in tracker.member_activities.items():
        member = inter.guild.get_member(member_id)
        if member:
            total_duration = tracker.get_total_duration(member_id)
            member_durations.append((member, total_duration, activities))
    
    member_durations.sort(key=lambda x: x[1], reverse=True)
    
    # Add member activity details
    for member, total_duration, activities in member_durations:
        activity_details = []
        for activity in activities:
            join_time = activity.join_time.astimezone(est).strftime('%I:%M:%S %p')
            leave_time = "Still Present" if activity.leave_time is None else \
                        activity.leave_time.astimezone(est).strftime('%I:%M:%S %p')
            activity_details.append(f"Join: {join_time} - Leave: {leave_time}")
        
        hours, remainder = divmod(total_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{hours}h {minutes}m {seconds}s"
        
        member_info = f"**{member.display_name}** ({member.name})\n"
        member_info += f"Total Duration: {duration_str}\n"
        member_info += "Activity:\n" + "\n".join(f"• {detail}" for detail in activity_details)
        
        embed.add_field(
            name=f"Member Activity",
            value=member_info,
            inline=False
        )
    
    await attendance_channel.send(embed=embed)
    del active_monitors[guild_id]
    await inter.response.send_message("Monitoring stopped and activity report has been generated.", ephemeral=True)

[Previous absent command remains unchanged...]

# Bot token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)