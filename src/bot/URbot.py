#!/opt/virtualenv/URBot/bin/python

import inspect
import logging
import os
import platform
import sys
import importlib
from importlib import resources

from discord.ext import commands

from urpy import MyHelpCommand
from urpy.utils import error_log, code_block, log
from bot import _, strings
from bot import localization

import urpy

debug = platform.system() == 'Windows'

from bot import info
from bot import settings
from bot.cog_General import General
from bot.cog_About import About

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com


class URBot(urpy.MyBot):
    """
    Discord bot for "l'Union des Rôlistes". Contains global settings
    and functions.

    Additional groups of functions can be added at runtime through
    the .add_cog method.
    """

    def __init__(self):
        """
        Creates an instance of URBot. Use the run method to start it.
        """
        self.localization = localization  # TODO move localization to urpy
        super(URBot, self).__init__(settings.command_prefix, help_command=MyHelpCommand(self.localization))
        self.cog_general = General(self)

        # adds base cogs to the bot
        self.add_cog(self.cog_general)
        self.add_cog(About(self))

        self.isDebugMode = debug

    @staticmethod
    def get_credits():
        """ Return creditted people. """
        return resources.read_text(info, 'credits.txt')

    @staticmethod
    def get_version():
        """ Return version number. """
        return resources.read_text(info, 'version.txt')

    @staticmethod
    def get_name():
        """ Return title of the bot."""
        return _(strings.bot_title)

    async def on_ready(self):
        """ Listener to the on_ready event. """
        error_log("We have logged in as {}!".format(self.user))

    async def invoke(self, ctx: commands.Context):
        self.localization.set_current_user(ctx.author.id)
        await super(URBot, self).invoke(ctx)

    async def on_command_error(self, context, exception: commands.CommandError):
        """ Listener to the on_command_error event. """  # TODO better docstring
        if isinstance(exception, commands.UserInputError):
            await context.send(_("{err_msg}\nIncorrect usage ☹ Check help of the command for more information.").format(
                err_msg=code_block(exception)))
        else:
            raise exception

    def add_to_command(self, command: str, *callbacks):
        """
        Add one or several callbacks to a cog_General discord command.

        @param command str
                name of the command (ex: 'edit')
        @callbacks callbacks iterator[functions]
                callbacls
        """
        self.cog_general.add_to_command(command, *callbacks)


if debug:
    cogs_path = os.path.abspath('cogs')
    token_path = '../../../bot_token'
else:
    cogs_path = '/usr/local/src/URbot/bot/cogs'
    token_path = '/usr/local/src/URbot/.bot_token'


def main():
    logging.basicConfig(level=logging.INFO)
    ur_bot = URBot()
    log("Loading cogs...")
    # adds the "cogs" folder to the import path
    sys.path.append(cogs_path)

    if os.path.exists(cogs_path):
        # scans the "cogs" folder for cogs to add to the bot
        for dir_entry in os.scandir(cogs_path):
            dir_entry: os.DirEntry

            # imports and adds all found cogs
            if dir_entry.is_dir() and dir_entry.name != '__pycache__' and not dir_entry.name.startswith('.'):

                # tries to import the cog module
                try:
                    module = importlib.import_module(f"{dir_entry.name}.cog")

                except ValueError as e:  # TODO fix error handling
                    error_log(
                        f"The package \'{dir_entry.name}\' does not contain a module named \'cog.py\' (in {dir_entry.path}).")

                else:
                    # retrieves all discord.Cog based classes
                    cog_classes = filter(lambda member: inspect.isclass(member[1]) and issubclass(member[1], commands.Cog),
                                         inspect.getmembers(module))
                    for Cog in cog_classes:
                        # adds cog to the bot
                        cog = Cog[1](ur_bot)
                        ur_bot.add_cog(cog)
                        log(f"Loaded : {cog.qualified_name}")
        log("Done")
    else:
        log("No cogs found")

    # reads the bot token
    with open(token_path) as f:
        bot_token = f.read()

    # starts the bot
    ur_bot.run(bot_token)


if __name__ == '__main__':
    main()
