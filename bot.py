import discord
from discord.ext import commands
import os

# Fetch the Discord token from Heroku Config Vars
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}!")
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Load extensions (cogs)
async def load_extensions():
    initial_extensions = ["admin_cog", "attendance_cog", "absence_cog", "schedule_cog"]
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension} successfully.")
        except Exception as e:
            print(f"Failed to load {extension}: {e}")

bot.loop.run_until_complete(load_extensions())
bot.run(TOKEN)