import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
BOT_PREFIX = os.getenv('BOT_PREFIX', '$')

HELP_DATA = {
    "About":
    {
        "cmd_0":
        {
            "cmd": "credit",
            "help": "Affiche les crédits"
        },

        "cmd_1":
        {
            "cmd": "version",
            "help": "Affiche les numéros de version"
        },
    },

    "General":
    {
        "cmd_0":
        {
            "cmd": "cancel",
            "help": "Annule l'action en cours"
        },

        "cmd_1":
        {
            "cmd": "done",
            "help": "Confirme l'action en cours"
        },

        "cmd_2":
        {
            "cmd": "edit",
            "help": "Édite un message"
        },

        "cmd_3":
        {
            "cmd": "lang",
            "help": "Change la langue de l'utilisateur"
        },
    },

    "Planning":
    {
        "cmd_0":
        {
            "cmd": "cal",
            "help": "Permet d'accéder au calendrier"
        },

        "cmd_1":
        {
            "cmd": "jdr",
            "help": "Envoie un lien pour créer une partie"
        },

        "cmd_2":
        {
            "cmd": "site",
            "help": "Permet d'accéder au calendrier"
        },

    },

    "Presentation":
    {
        "cmd_0":
        {
            "cmd": "prez",
            "help": "Envoie un lien pour se présenter"
        },
    },

    "No Category":
    {
        "cmd_0":
        {
            "cmd": "help",
            "help": "Affiche ce message"
        },
    }
}


def GetMaxStrSizeInArray(array: dict, callback=None):
    _size = 0
    for cmd in array:
        _r = callback(cmd)
        if (_r > _size):
            _size = _r
    return _size


async def on_message(event, *args, **kwargs):
    if event.content.startswith('hi'):
        await event.channel.send(f'Hello! Mis a jour : {args}')


async def on_help(event, *args):
    embed = discord.Embed(title="URBOT - helper", color=0x0CC1EE)
    embed.set_author(
        name="UR-BOT", icon_url="https://cdn.discordapp.com/avatars/1040275175687606372/33d5a8782c1d658caeeae59799e722b0.webp?size=32")
    HELP = str(f"**prefix :    {BOT_PREFIX}**\n\n\t```diff\n")
    for x in HELP_DATA.items():
        HELP += f"\r+ {x[0]}\n\n\t"
        # Obtenir la chaine la plus longe pour ensuite center la fleche (->)
        c = GetMaxStrSizeInArray(x[1].items(), lambda a: a[1]['cmd'].__len__())
        for cmd in x[1].items():
            _offset = (c - cmd[1]["cmd"].__len__()) + \
                1  # centrage de lq flèche (->)
            # Ecrit la command -> description
            HELP += cmd[1]["cmd"] + (" "*_offset) + "-> "+cmd[1]["help"]+"\n\t"
    HELP += f"\n```"
    embed.add_field(
        name="**\n**", value="**───────────────────────────────**", inline=False)
    embed.add_field(name="**\n**", value=HELP, inline=False)
    embed.set_footer(text="Union Roliste commands helper.",
                     icon_url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4")
    # set le logo en haut a droit
    embed.set_thumbnail(
        url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4")
    await event.channel.send(embed=embed)


class Tmp(commands.Cog, name='tmp'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def cog_load(self):  # called when the cog is loaded
        print(self.__class__.__name__ + " is loaded")

    @commands.command(name="_help")
    async def help(Self, ctx):
        await on_help(ctx)

    @commands.command(aliases=['reload', 'rld'])
    async def reload_module(Self, ctx):
        await reload_module()
        await ctx.channel.send("The scripts has been reloaded.")
        return 0


async def setup(bot):
    await bot.add_cog(Tmp(bot))
