import sys
import asyncio
import importlib
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
VERSION = os.getenv('BOT_BASE_VERSION')

sys.path.append('..')


class Base(commands.Cog, name='base'):
    def __init__(self, bot):
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
        txt = f'URBot_base version : {VERSION}'
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

    @commands.command(name="_help", help='affiche la version du bot', aliases=['h'], )
    async def on_help(self, event):
        help = f""
        await event.channel.send(help)

    # async def on_help(self, event):
    #     HELP = str(f"```diff\n\nprefix : {BOT_PREFIX}\n\n")
    #     # Obtenir la chaine la plus longe pour ensuite center la fleche (->)
    #     c = GetMaxCommandSize(bot_instance.walk_commands())
    #     for command in bot_instance.walk_commands():  # pour chaque commandes
    #         fullcmd = (command.name+(" ("+",".join(command.aliases) +
    #                                  ") " if (command.aliases != []) else ""))
    #         _offset = (c["size"] - fullcmd.__len__()) + \
    #             1  # centrage de la flèche (->)
    #         if (command.name and command.help):
    #             fullcmd += (" "*_offset) + "-> "+command.help
    #             if (command.description in [*c["type"].keys()]):
    #                 # Ajout la command à la description actuel (About, Presentation, No Category)
    #                 c["type"][command.description].append(fullcmd)
    #     for category in c["type"]:  # prépare le text final qui sera afficher
    #         HELP += category+":"  # ajout la cqtégory
    #         # pour chaque command dans la catégory qlors on l'ajout au text final (HELP)
    #         for help in c["type"][category]:
    #             HELP += "\n"+"\t"+help
    #         HELP += "\n\n"
    #     HELP += f"Entrez $help commande pour plus d'info sur une commande.\nVous pouvez aussi entrer $help categorie pour plus d'info sur une catégorie.```"
    #     await event.channel.send(HELP)


async def setup(bot):
    await bot.add_cog(Base(bot))


# def version():
#     return f'URBot_base version : {VERSION}'
