import re
import discord
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

def parse_seconds_to_hms(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    result = f"{hours}h {minutes}m {seconds}s"
    logger.debug(f"Parsed {seconds} seconds to {result}")
    return result

def parse_duration(duration_str):
    match = re.match(r'(\d+)\s*(s|secs?|seconds?|m|mins?|minutes?|h|hrs?|hours?|d|days?)', duration_str, re.IGNORECASE)
    if not match:
        logger.warning(f"Failed to parse duration: {duration_str}")
        return None
    value, unit = match.groups()
    value = int(value)
    unit = unit.lower()
    if 's' in unit:
        result = value
    elif 'm' in unit:
        result = value * 60
    elif 'h' in unit:
        result = value * 3600
    elif 'd' in unit:
        result = value * 86400
    else:
        result = None
    logger.debug(f"Parsed duration '{duration_str}' to {result} seconds")
    return result

def parse_mentions(ctx, mentions):
    mention_list = mentions.split()
    members = []

    for mention in mention_list:
        mention = mention.strip()
        if mention.startswith('<@&'):  # Role mention
            role_id = int(mention.strip('<@&>'))
            role = ctx.guild.get_role(role_id)
            if role:
                members.extend(role.members)
                logger.debug(f"Added {len(role.members)} members from role {role.name}")
        elif mention.startswith('<@!') or mention.startswith('<@'):  # User mention
            user_id = int(mention.strip('<@!>').strip('<@>'))
            member = ctx.guild.get_member(user_id)
            if member:
                members.append(member)
                logger.debug(f"Added member {member.name}")
    
    unique_members = list(set(members))
    logger.info(f"Parsed {len(mention_list)} mentions into {len(unique_members)} unique members")
    return unique_members

def is_manager(ctx):
    guild_id = ctx.guild.id
    if guild_id not in ctx.bot.manager_roles:
        ctx.bot.manager_roles[guild_id] = []
    if guild_id not in ctx.bot.manager_members:
        ctx.bot.manager_members[guild_id] = []
    
    user_roles = ctx.author.roles
    is_manager = (ctx.author.guild_permissions.administrator or 
                  any(role.id in ctx.bot.manager_roles[guild_id] for role in user_roles) or 
                  ctx.author.id in ctx.bot.manager_members[guild_id])
    logger.debug(f"Checked if user {ctx.author.name} is manager: {is_manager}")
    return is_manager