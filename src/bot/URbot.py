#!/opt/virtualenv/URBot/bin/python
import logging
import re
import sys
from discord.ext import commands

# sys.path.append("D:\\Florian\\Documents\\_Documents\\Projets\\Union_Rolistes\\URbot\\planning\\src")
from importlib import resources
import info
import template
#from planning.cog import Planning
from pathlib import Path
from bot_cog import About
#from presentation.cog import Presentation

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
    #ur_bot.add_cog(Planning(ur_bot))
    #ur_bot.add_cog(Presentation())

    with open("/root/.bot_token", 'r') as f:
        bot_token = f.read()

    ur_bot.run(bot_token)
