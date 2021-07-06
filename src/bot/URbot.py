#!/opt/virtualenv/URBot/bin/python
import importlib
import inspect
import logging
import os
import re
import sys
from discord.ext import commands
import importlib
# sys.path.append("D:\\Florian\\Documents\\_Documents\\Projets\\Union_Rolistes\\URbot\\cog_planning\\src")
from importlib import resources
import info
import template

from pathlib import Path
from cog_About import About


class URBot(commands.Bot):
    def __init__(self):
        super(URBot, self).__init__('$')
        self.add_cog(About(self))

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


if __name__ == '__main__':
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
