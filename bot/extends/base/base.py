import sys
import asyncio
import importlib
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

sys.path.append('..')

# class base with case insensitive


class Base(commands.Cog, name='Base'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    async def cog_load(self):  # called when the cog is loaded
        print(self.__class__.__name__ + " is loaded")

    @commands.command(name="ping", help='ping pong with the bot', aliases=['pong', 'p'], )
    @commands.guild_only()
    async def _ping(self, event):
        await asyncio.gather(  # concurent await
            event.message.add_reaction('🏓'),
            event.send('Pong! 🏓 {0} ms'.format(
                round(self.bot.latency, 3) * 1000))
        )

    @commands.command(name="credits", help='affiche les credits', aliases=['credit', 'c'], )
    async def _credits(self, event):
        credits = "```properties\n"
        # get directory path
        pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # load local credits first
        try:
            with open(f'{pwd}/credits.txt', 'r') as f:
                credits += f.read()
        except Exception as e:
            print(e)
        # for each directory
        for directory in os.listdir(pwd):
            # read credits file
            try:
                with open(f'{pwd}/{directory}/credits.txt', 'r') as f:
                    credits += '\n' + f.read()
            except Exception as e:
                print(e)
        await event.send(credits+'```')

    # send version of the bot
    @commands.command(name="version", help='affiche la version du bot', aliases=['v'], )
    async def _version(self, event):
        txt = version()
        # get directory path
        pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # for each directory
        for directory in os.listdir(pwd):
            # for each file in the directory
            for file in os.listdir(f'{pwd}/{directory}'):
                # if the file is a python file
                if file.endswith('.py') and not file.startswith('__'):
                    # get the file name without the extension
                    file_name = file[:-3]
                    # try import the function version in the file
                    try:
                        print(
                            f'try run : extends.{directory}.{file_name}.version()')
                        module = importlib.import_module(
                            f'extends.{directory}.{file_name}').version()
                        try:
                            txt += f'\n{module}'
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
        await event.send(txt)

    @commands.command(name="help", help='affiche les commandes, aliases, et descripton', aliases=['h', '?'])
    async def _help(self, event):
        # get all commands and sort them by category
        commandsByCat = {}
        for command in self.bot.walk_commands():
            if command.cog_name not in commandsByCat:
                commandsByCat[command.cog_name] = []
            commandsByCat[command.cog_name].append(command)
        # sort categories by key
        commandsByCat = dict(sorted(commandsByCat.items()))
        # sort commands by name alphabetically in each category
        for cat in commandsByCat:
            commandsByCat[cat] = sorted(
                commandsByCat[cat], key=lambda x: x.name)
        # create help message
        help = (f"```ansi\n"
                f"[2;34;4mprefix[0m [2;31m{self.bot.command_prefix}[0m\n")
        # add category and commands to the message
        for cat in commandsByCat:
            # example : "category : "
            help += f"\n[2;34;4m{cat}[0m : \n"
            for command in commandsByCat[cat]:
                # examle : "    command [alias] : help"
                aliases = f'''{' ' + str(command.aliases).replace("'", "") if command.aliases != [] else ''}'''
                msg = f' -- [2;36m{command.help}[0m' if command.help != None else ''
                help += f"  [2;33m{command.name}[0m{aliases}[0m{msg}\n"
        help += "```"
        await event.channel.send(help)


async def setup(bot):
    # remove old help
    bot.remove_command('help')
    await bot.add_cog(Base(bot))


def version():
    try:
        # Lecture du fichier
        with open('version.txt', 'r') as f:
            VERSION = f.read()
        return f'URBot_base version : {VERSION}'
    except FileNotFoundError:
        return 'Erreur : le fichier version.txt est introuvable.'
    except Exception as e:
        return f'Erreur lors de la lecture du fichier : {str(e)}'
