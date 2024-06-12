#!/usr/bin/env python
""" Minor League E-Sports Bot Commands
# Author: irox_rl
# Purpose: General Functions and Commands
# Version 1.0.4
"""

# local imports #

# non-local imports
import datetime
import discord
from discord.ext import commands
import time

""" System Error Strings 
"""
ERR_NO_PERMS = 'You do not have sufficient permissions to perform this action. Please contact someone with higher permissions than yours.'


class Commands(commands.Cog):
    def __init__(self,
                 master_bot,
                 ):
        self.bot = master_bot

    @commands.command(name='echo', description='echo')
    async def echo(self,
                   ctx: discord.ext.commands.Context,
                   *_str: str):
        await ctx.send(' '.join(_str))

    @commands.command(name='datetounix',
                      description='convert date to unix code for discord purposes.\n'
                                  'You must give a date in the following format: y/m/d H:M:S')
    async def datetounix(self,
                         ctx: discord.ext.commands.Context,
                         *date: str):
        try:
            _date = ' '.join(date)
            d = datetime.datetime.strptime(_date, '%y/%m/%d %H:%M:%S')
            unix_time = time.mktime(d.timetuple())
            await ctx.send(f'template: t:{str(int(unix_time))}:F  (remember to add < and > around the template!')
            await ctx.send(f'<t:{int(unix_time)}:F>')
        except ValueError:
            await ctx.reply('You must give a date in the following format:\n'
                            '%y/%m/%d %H:%M:%S\n'
                            'do not include am/pm. use 24 hour clock.')

    @commands.command(name='help', description="Show all available commands for this bot.")
    async def help(self, ctx: discord.ext.commands.Context):
        if ctx.channel is not discord.DMChannel:
            if self.bot.public_commands_channel is None or ctx.channel is not self.bot.public_commands_channel:
                if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                    if ctx.channel not in self.bot.extended_public_commands_channels:
                        return
        embed = self.bot.default_embed('**Available Bot Commands**\n\n',
                                       'All commands are prefaced with "ub."\n\n')
        embed.description += '\n'.join(
            sorted([f'**ub.{command}** - {command.description}' for command in self.bot.commands]))
        await ctx.reply(embed=embed)

    @commands.command(name="info", description="Get build info.")
    async def info(self, ctx):
        if ctx.channel is not discord.DMChannel:
            if self.bot.public_commands_channel is None or ctx.channel is not self.bot.public_commands_channel:
                if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                    return
        return await ctx.reply(embed=self.bot.info_embed())

    @commands.command(name='test', description='developer test function')
    async def test(self,
                   ctx: discord.ext.commands.Context):
        d = datetime.date(2024, 8, 16)
        unix_time = time.mktime(d.timetuple())
        await ctx.send(f'<t:{int(unix_time)}:F>')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if 'nice' == message.content.lower():
            await message.reply('nice')
