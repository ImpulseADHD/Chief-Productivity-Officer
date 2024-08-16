import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.reactions = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)
        self.initial_extensions = [
            'cogs.checkin'  # Ensure this is correctly pointing to the location of your Checkin cog
        ]

    async def setup_hook(self):
        # Load all the cogs/extensions safely
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"Loaded extension '{extension}' successfully.")
            except Exception as e:
                print(f"Failed to load extension '{extension}': {e}")

        # Synchronize the command tree across all guilds
        await self.tree.sync()
        print("Slash commands synchronized across all servers.")

    async def on_ready(self):
        print(f'{self.user} is ready!')
        print(f'Active in {len(self.guilds)} guilds:')
        for guild in self.guilds:
            print(f' - {guild.name} (ID: {guild.id})')

    async def close(self):
        await super().close()
        print("Bot has been shut down gracefully.")

if __name__ == '__main__':
    bot = Bot()
    bot.run(TOKEN)
