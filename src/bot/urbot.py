#!/opt/virtualenv/URBot/bin/python
"""Ce programme initialise et lance le bot URBot."""

import os
import platform
import sys
import logging
import inspect
from importlib import resources, import_module
from discord.ext import commands
from Bot_Base.src.urpy import localization
from Bot_Base.src.urpy.help import MyHelpCommand
from Bot_Base.src.urpy.my_commands import MyBot
from Bot_Base.src.urpy.utils import error_log, code_block, log
from Bot_Base.src.bot import info
from cog_about import About
from cog_general import General
import settings
import strings

debug = platform.system() == 'Windows'


# UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# Ask a derogation at Contact.unionrolistes@gmail.com


class URBot(MyBot):
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
        super(URBot, self).__init__(settings.COMMAND_PREFIX, help_command=MyHelpCommand(self.localization))
        self.cog_general = General(self)

        # adds base cogs to the bot
        self.add_cog(self.cog_general)
        self.add_cog(About(self))

        self.is_debug_mode = debug

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
        return strings.BOT_TITLE

    async def on_ready(self):
        """ Listener to the on_ready event. """
        error_log("We have logged in as {}!".format(self.user))

    async def invoke(self, ctx: commands.Context):
        localisation = localization.Localization()
        self.localization.Localization.set_current_user(localisation, ctx.author.id)
        await super(URBot, self).invoke(ctx)

    async def on_command_error(self, context, exception: commands.CommandError):
        """ Listener to the on_command_error event. """  # TODO better docstring
        if isinstance(exception, commands.UserInputError):
            err_msg = code_block(exception)
            await context.send(f"{err_msg}\nIncorrect usage ☹ Check help of the command for more information.")
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
    COGS_PATH = os.path.abspath('cogs')
    TOKEN_PATH = '../../../bot_token'
else:
    COGS_PATH = '/usr/local/src/URbot/bot/cogs'
    TOKEN_PATH = '/usr/local/src/URbot/.bot_token'


def main():
    """
    Initialise et lance le bot Discord URBot.

    Cette fonction configure le système de logging, charge tous les cogs Discord
    depuis le répertoire spécifié (COGS_PATH), les ajoute au bot, lit le jeton du
    bot depuis TOKEN_PATH, et démarre le bot avec le jeton récupéré.

    Étapes :
    1. Configure le logging au niveau INFO.
    2. Initialise une instance de URBot.
    3. Ajoute le dossier 'cogs' au chemin d'importation Python.
    4. Analyse le dossier 'cogs' pour trouver les modules Python contenant des cogs Discord.
    5. Importe et ajoute chaque cog trouvé à l'instance du bot.
    6. Enregistre le chargement réussi de chaque cog.
    7. Lit le jeton du bot Discord depuis TOKEN_PATH.
    8. Lance le bot en utilisant le jeton récupéré.

    Lance :
        ValueError : Si un module dans COGS_PATH ne contient pas de fichier 'cog.py'.

    Remarque :
        Assurez-vous que COGS_PATH et TOKEN_PATH sont correctement définis avant d'exécuter cette fonction.
    """

    logging.basicConfig(level=logging.INFO)
    ur_bot = URBot()
    log("Loading cogs...")
    # adds the "cogs" folder to the import path
    sys.path.append(COGS_PATH)

    if os.path.exists(COGS_PATH):
        # scans the "cogs" folder for cogs to add to the bot
        for dir_entry in os.scandir(COGS_PATH):
            dir_entry: os.DirEntry

            # imports and adds all found cogs
            if dir_entry.is_dir() and dir_entry.name != '__pycache__' and not dir_entry.name.startswith('.'):

                # tries to import the cog module
                try:
                    module = import_module(f"{dir_entry.name}.cog")

                except ValueError as e:  # TODO fix error handling
                    error_log(
                        f"The package \'{dir_entry.name}\' does not contain a module named \'cog.py\' (in {dir_entry.path}. //{e}")

                else:
                    # retrieves all discord.Cog based classes
                    cog_classes = filter(
                        lambda member: inspect.isclass(member[1]) and issubclass(member[1], commands.Cog),
                        inspect.getmembers(module))
                    for cog in cog_classes:
                        # adds cog to the bot
                        cog = cog[1](ur_bot)
                        ur_bot.add_cog(cog)
                        log(f"Loaded : {cog.qualified_name}")
        log("Done")
    else:
        log("No cogs found")

    # reads the bot token
    with open(TOKEN_PATH) as f:
        bot_token = f.read()

    # starts the bot
    ur_bot.run(bot_token)


if __name__ == '__main__':
    main()
