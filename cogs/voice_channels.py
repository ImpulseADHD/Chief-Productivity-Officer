import discord
from discord import app_commands
from discord.ext import commands
from utils import app_is_manager, is_group_creator
import logging

logger = logging.getLogger(__name__)

class VoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("VoiceChannels cog initialized")

    @app_commands.command(name="create_vc", description="Create a voice channel for the study group")
    @app_commands.describe(name="Name of the voice channel (optional)")
    @is_group_creator()
    @app_is_manager()
    async def create_vc(self, interaction: discord.Interaction, name: str = None):
        logger.info(f"create_vc command invoked by {interaction.user}")
        group = await self.bot.db.get_study_group(interaction.guild_id)
        if not group:
            logger.warning(f"No study group exists in server {interaction.guild_id}")
            await interaction.response.send_message("No study group exists in this server.", ephemeral=True)
            return

        if group[8]:  # Assuming voice_channel_id is at index 8
            logger.warning(f"Voice channel already exists for group {group[0]}")
            await interaction.response.send_message("A voice channel already exists for this group.", ephemeral=True)
            return

        channel_name = name or f"{group[1]} VC"
        logger.debug(f"Creating voice channel '{channel_name}'")
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(connect=False),
            interaction.guild.me: discord.PermissionOverwrite(connect=True, manage_channels=True)
        }

        _, session_role_id = await self.bot.db.get_group_roles(group[0])
        session_role = interaction.guild.get_role(session_role_id)
        if session_role:
            overwrites[session_role] = discord.PermissionOverwrite(connect=True)
            logger.debug(f"Added connect permission for role {session_role.name}")

        try:
            channel = await interaction.guild.create_voice_channel(channel_name, overwrites=overwrites)
            await self.bot.db.update_voice_channel(group[0], channel.id)
            logger.info(f"Voice channel {channel.id} created for group {group[0]}")
            await interaction.response.send_message(f"Voice channel {channel.mention} created for the study group.")
        except discord.HTTPException as e:
            logger.error(f"Failed to create voice channel: {str(e)}")
            await interaction.response.send_message("Failed to create the voice channel. Please try again later.", ephemeral=True)

    @app_commands.command(name="delete_vc", description="Delete the voice channel for the study group")
    @is_group_creator()
    @app_is_manager()
    async def delete_vc(self, interaction: discord.Interaction):
        logger.info(f"delete_vc command invoked by {interaction.user}")
        group = await self.bot.db.get_study_group(interaction.guild_id)
        if not group or not group[8]:  # Assuming voice_channel_id is at index 8
            logger.warning(f"No voice channel exists for group in server {interaction.guild_id}")
            await interaction.response.send_message("No voice channel exists for this group.", ephemeral=True)
            return

        channel = interaction.guild.get_channel(group[8])
        if channel:
            try:
                await channel.delete()
                await self.bot.db.update_voice_channel(group[0], None)
                logger.info(f"Voice channel {channel.id} deleted for group {group[0]}")
                await interaction.response.send_message("Voice channel deleted.")
            except discord.HTTPException as e:
                logger.error(f"Failed to delete voice channel: {str(e)}")
                await interaction.response.send_message("Failed to delete the voice channel. Please try again later.", ephemeral=True)
        else:
            logger.warning(f"Voice channel {group[8]} no longer exists for group {group[0]}")
            await self.bot.db.update_voice_channel(group[0], None)
            await interaction.response.send_message("The voice channel no longer exists.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logger.debug(f"Voice state update: {member} moved from {before.channel} to {after.channel}")
        if before.channel and not after.channel:
            group = await self.bot.db.get_study_group(before.channel.guild.id)
            if group and group[8] == before.channel.id:
                logger.debug(f"Member {member} left study group voice channel {before.channel.id}")
                if not before.channel.members:
                    try:
                        await before.channel.delete()
                        await self.bot.db.update_voice_channel(group[0], None)
                        logger.info(f"Deleted empty voice channel {before.channel.id} for group {group[0]}")
                    except discord.HTTPException as e:
                        logger.error(f"Failed to delete empty voice channel: {str(e)}")

async def setup(bot):
    await bot.add_cog(VoiceChannels(bot))
    logger.info("VoiceChannels cog loaded")