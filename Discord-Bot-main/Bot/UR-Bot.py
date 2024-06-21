import discord
from dotenv import load_dotenv
import DebugBot
from discord.ext import commands
import os
import aiohttp

load_dotenv()
TOKEN = os.getenv('TOKEN')


# Fonction pour lire la description depuis le fichier
def read_description_from_file():
    try:
        with open('description.txt', 'r') as file:
            # ↓ De quel fichier ?, ↓ Quelle permission ?
            return file.read().strip()
    except FileNotFoundError:
        return ""


# Fonction pour écrire la description dans le fichier
def write_description_to_file(texte):
    with open('description.txt', 'w') as file:
        # ↓ De quel fichier ?, ↓ Quelle permission ?
        file.write(texte)


class UR_BOT(commands.Bot):

    async def on_ready(self):
        print('--- We have successfully loggged in as {0.user}'.format(self))

        # Lire la description depuis le fichier et mettre à jour la présence du bot
        bot.description = read_description_from_file()
        await update_bot_presence()

    async def on_message(self, message):
        if message.author == self.user:
            return

        await DebugBot.debug_on_message(message)

        return await bot.process_commands(message)


intent = discord.Intents.default()
intent.members = True
intent.messages = True

bot = UR_BOT(command_prefix=DebugBot.event.BOT_PREFIX, intents=intent)
bot.remove_command('help')



# Commande pour changer le pseudo du bot
@bot.command()
async def name(ctx, *, new_name: str):
    server_id = ctx.guild.id

    try:
        guild = bot.get_guild(server_id)

        if guild:
            # Changer le pseudo du bot sur le serveur spécifié
            await guild.me.edit(nick=new_name)
            await ctx.send(f"Le pseudo du bot a bien été changé en {new_name}.")
        else:
            await ctx.send("Impossible de trouver le serveur spécifié.")

    except discord.HTTPException as e:
        await ctx.send("Une erreur s'est produite lors du changement de pseudo du bot. Veuillez regarder la console.")
        print(e)


# Fonction qui met à jour automatiquement (et en permanance) le statut personnalisé du bot.
async def update_bot_presence():
    activity = discord.Game(name=bot.description)  # Ces deux lignes doivent être appelées en permanance par
    await bot.change_presence(activity=activity)  # la fonctionon_ready. C'est pourquoi elles ne sont pas écrites dans
    # la commande 'description'.


# Commande pour changer le statut personnalisé du bot.
@bot.command()
async def description(ctx, *, texte: str):
    bot.description = texte
    write_description_to_file(texte)
    await update_bot_presence()
    await ctx.send(f"La description du bot a été mise à jour.")


# Commande pour changer la photo de profil du bot.
@bot.command()
async def pfp(ctx, *, url: commands.clean_content):
    try:
        server_id = ctx.guild.id
        guild = bot.get_guild(server_id)

        if guild:
            # Récupération de l'image.
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:  # Malgré l'erreur, le code fonctionne toujours.
                    if resp.status != 200:
                        return await ctx.send(f"Impossible de télécharger l'image. Statut HTTP : {resp.status}")

                    # La photo de profil prend la forme de l'image.
                    data = await resp.read()
                    await bot.user.edit(avatar=data)
                    await ctx.send("Photo de profil mise à jour. Redémarrez le bot pour voir le résultat.")
        else:
            # Attraper toutes les erreurs possibles.
            await ctx.send("Impossible de trouver le serveur discord spécifié. Veuillez contactez les développeurs du projet.")
    except aiohttp.InvalidURL:
        await ctx.send("L'URL fournie est invalide. Veuillez vérifier qu'elle ne contient pas de guillemet, "
                       "ni d'apostrophe et réessayer.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {str(e)} Vérifiez votre configuration du bot ou contactez "
                       f"les développeurs du projet.")


@bot.command()
@commands.guild_only()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong ! {latency}ms")


@bot.command(name="help")
async def help(ctx):
    await DebugBot.debug_on_help(ctx)


@bot.command(name="prez")
async def prez(ctx):
    await DebugBot.debug_on_prez(ctx)


@DebugBot.update_all_modules
async def reload_module():
    return 0


@bot.command(aliases=['reload', 'rld'])
async def reload_module(ctx):
    await reload_module()
    await ctx.channel.send("The scripts has been reloaded.")
    return 0


bot.run(TOKEN)
