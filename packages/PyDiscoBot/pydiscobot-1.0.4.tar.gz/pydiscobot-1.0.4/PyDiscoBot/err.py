#!/usr/bin/env python
""" error
# Author: irox_rl
# Purpose: show errors? also register callback for error messages
# Version 1.0.3
"""

# local imports #

# non-local imports
from discord.ext import commands

from typing import Callable

err_callback: Callable = None


class InsufficientPrivilege(commands.CheckFailure):
    pass


class IllegalChannel(commands.CheckFailure):
    pass


async def err(message: str | Exception) -> None:
    """ Helper function to send error or notification messages to notify channel with a single parameter.\n
        **If a notification channel does not exist**, the notification is printed to console instead\n
        **param message**: message to report\n
        **returns**: None\n
        """
    global err_callback
    if not message:
        return
    if not err_callback:
        return print(message)
    await err_callback(message)


def register_callback(callback: Callable):
    global err_callback
    err_callback = callback
