#!/opt/virtualenv/URBot/bin/python

import inspect
import logging
import os
import sys
sys.path.append("/usr/local/bin/")
import importlib
from importlib import resources

import urpy
from discord.ext import commands

from bot import info
from bot import settings
from bot.cog_General import General
from cog_About import About


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
        super(URBot, self).__init__(settings.command_prefix)
        self.add_cog(About(self))
        self.general_cog = General(self)
        self.add_cog(self.general_cog)

    @staticmethod
    def get_credits():
        return resources.read_text(info, 'credits.txt')

    @staticmethod
    def get_version():
        """ Return version.txt of bot. """
        return resources.read_text(info, 'version.txt')

    @staticmethod
    def get_name():
        return resources.read_text(info, 'name.txt')

    async def on_ready(self):
        print("We have logged in as {}!".format(self.user))

    def add_to_command(self, command: str, *callbacks):
        self.general_cog.add_to_command(command, *callbacks)


def main():
    logging.basicConfig(level=logging.INFO)
    ur_bot = URBot()

    sys.path.append(os.path.abspath('cogs'))
    for dir_entry in os.scandir('cogs'):
        dir_entry: os.DirEntry
        if dir_entry.is_dir() and dir_entry.name != '__pycache__' and not dir_entry.name.startswith('.'):
            module = importlib.import_module(f"{dir_entry.name}.cog")
            for cog in filter(lambda mem: inspect.isclass(mem[1]) and issubclass(mem[1], commands.Cog), inspect.getmembers(module)):
                ur_bot.add_cog(cog[1](ur_bot))

    # with open("/root/.bot_token", 'r') as f:
    #     bot_token = f.read()
    with open("../../../bot_token") as f:
        bot_token = f .read()

    ur_bot.run(bot_token)


if __name__ == '__main__':
    main()
