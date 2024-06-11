#!/usr/bin/env python
""" Periodic Task
# Author: irox_rl
# Purpose: Periodic Task to run tasks as required per application
# Version 1.0.3
"""

# local imports #
from .channels import clear_channel_messages

# non-local imports
import datetime
import discord
from discord.ext import tasks
from typing import Callable


class PeriodicTask:
    """ Periodic Task
            This class uses ***@task***s to run tasks as required.
            """

    def __init__(self,
                 cycle_time: int,
                 master_bot,
                 task_callback: Callable = None,
                 enable_admin: bool = False):
        """ Initialize method\n
                            **param cycle_time**: time interval (in seconds) for the periodic task to run\n
                            **param master_bot**: reference of the Bot this task belongs to; for callbacks\n
                            **param enable_admin**: enable_admin functions to be performed by this bot\n
                            **param admin_channel**: admin channel that this bot can post admin info to\n
                            **param roster_channel**: roster channel that this bot can post roster info to\n
                            All data is initialized to zero. Franchise load will be called 'on_ready' of the bot\n
                            **returns**: None\n
                        """
        self.callback: Callable = task_callback
        self.admin_message: discord.Message | None = None
        self.bot = master_bot
        self.cycle_time: int = cycle_time
        self._enable_admin: bool = enable_admin
        self._initialized: bool = False
        self.on_tick: [Callable] = []
        self.ticks: int = 0

    @property
    def initialized(self):
        return self._initialized

    @tasks.loop()
    async def run(self):
        """ looping task\n
            **returns**: None\n
            """
        await self.admin()
        await self.callback()

    async def __regen_admin__(self):
        """ helper function to clear out and repost admin information\n
        **returns**: None\n
        """
        """ if there is no admin channel, do not run
        """
        if not self.bot.admin_channel or not self._enable_admin:
            return

        """ clear out channel messages
        """
        await clear_channel_messages(self.bot.admin_channel, 100)

        """ generate new admin message and record it
        """
        self.admin_message = await self.bot.admin_channel.send(embed=self.bot.info_embed())

    def __time__(self):
        """ periodic task time function\n
                    **returns**: None\n
                    """
        self.bot._last_time = self.bot._time if self.bot._time else datetime.datetime.now()
        self.bot._time = datetime.datetime.now()
        self.bot.new_weekday = True if self.bot._time.weekday() != self.bot._last_time.weekday() else False
        self.bot.new_week = True if self.bot._time.isocalendar().week != self.bot._last_time.isocalendar().week else False

    async def admin(self):
        """ periodic task admin function\n
            **returns**: None\n
            """
        self.ticks += 1
        self.__time__()

        for callback in self.on_tick:
            callback(self.ticks)

        self._initialized = True

        if self._enable_admin and self.bot.admin_channel:
            try:
                await self.admin_message.edit(embed=self.bot.info_embed())
            except discord.errors.NotFound:
                await self.__regen_admin__()
            except AttributeError:
                await self.__regen_admin__()
            except discord.errors.DiscordServerError:
                await self.__regen_admin__()

    def change_interval(self,
                        seconds: int) -> None:
        """ change interval of periodic task\n
        **param seconds**: period that the task will sleep between intervals\n
        **returns**: self\n
        """
        self.cycle_time = seconds
        self.run.change_interval(seconds=self.cycle_time)
