from dotenv import load_dotenv
import DebugBot
import os
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')


class UrBot(commands.Bot):
    """
    Classe initialisée à chaque lancement du BOT.
    """
    async def on_ready(self):
        """
        Éxécution d'une action au lancement du BOT.
        """
        print('--- We have successfully logged in as {0.user}'.format(self))

    async def on_message(self, message):
        """
        Est une méthode qui permet :
            - d'ignorer les messages envoyés par le BOT lui-même ;
            - d'appeler une fonction de débogage pour chaque message entrant ;
            - de traiter et d'exécuter les commandes des utilisateurs.
        """
        if message.author == self.user:
            return

        await DebugBot.debug_on_message(message)

        return await BOT.process_commands(message)


INTENT = discord.Intents.default()
INTENT.members = True
INTENT.messages = True
BOT = UrBot(command_prefix=DebugBot.event.BOT_PREFIX, intents=INTENT)
BOT.remove_command('help')


@BOT.command()
@commands.guild_only()
async def ping(ctx):
    """
    Calcul de la latence de l'utilisateur (additionnée à celle des serveurs discord) et renvoie de cette dernière.
    """
    latency = round(BOT.latency * 1000)
    await ctx.send(f"Pong ! {latency}ms")


@BOT.command(name="help")
async def help(ctx):
    """
    Appel d'une méthode quand la commande est reçue.
    """
    await DebugBot.debug_on_help(ctx)


@BOT.command(name="prez")
async def prez(ctx):
    """
    Appel d'une méthode quand la commande est reçue.
    """
    await DebugBot.debug_on_prez(ctx)


# Fonction utilisée dans "reload_module".
@DebugBot.update_all_modules
async def reload_all_modules():
    """
    Retourne 0.
    """
    return 0


# Commande Discord pour recharger les modules
@BOT.command(aliases=['reload', 'rld'])
async def reload_module(ctx):
    """
    Appel d'une méthode quand la commande est reçue.
    """
    await reload_all_modules()
    await ctx.channel.send("The scripts have been reloaded.")
    return 0

BOT.run(TOKEN)
