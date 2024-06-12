#!/usr/bin/env python
""" Channels functions
# Author: irox_rl
# Purpose: General Functions of discord channels
# Version 1.0.3
"""

# local imports #

# non-local imports
import discord


async def clear_channel_messages(channel: discord.channel,
                                 count: int) -> bool:
    """ Helper function to clear a channel of messages\n
        Max channel message delete count is 100\n
        **param channel**: the channel to delete messages from\n
        **param count**: number of messages to delete
        """
    """ If count is out of bounds, return 
    """
    if count > 100 | count <= 0:
        raise ValueError(f'Cannot delete that many messages!: {count}')
    """ Attempt to delete message from discord server channel specified
        Catch exceptions specific by discord API method and return
    """
    try:
        await channel.delete_messages([message async for message in channel.history(limit=count)])
        return True
    except discord.ClientException:
        return False
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return False


def get_channel_by_id(channel_id: str,
                      guild: discord.Guild) -> discord.abc.GuildChannel | None:
    """ Get specific Guild Channel by passed ID """
    return next((x for x in guild.channels if x.id.__str__() == channel_id), None)


async def get_channel_message_by_id(channel: discord.TextChannel | discord.abc.GuildChannel,
                                    message_id: str) -> discord.Message | None:
    """ Get a specific message in a specified channel by passed ID """
    return next((x for x in [message async for message in channel.history(limit=200)] if x.id.__str__() == str(message_id)),
                None)


async def post_image(channel: discord.channel,
                     picture_file: str):
    """ Post an image to a specified channel """
    with open(picture_file, 'rb') as f:
        # noinspection PyTypeChecker
        picture = discord.File(f)
        await channel.send(file=picture)
