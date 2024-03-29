
import asyncio
import discord

BOT_PREFIX = "$"


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

};


def GetMaxStrSizeInArray(array:dict,callback=None):
    _size=0;
    for cmd in array:
        _r = callback(cmd)
        if(_r > _size):
           _size = _r
    return _size


async def on_ping(event):
        await event.author.send("pong");

        

async def on_message(event,*args,**kwargs):
    if event.content.startswith('hi'):
        await event.channel.send(f'Hello! Mis a jour : {args}')

async def on_prez(event,*args,**kwargs):
    embed = discord.Embed(url="http://presentation.unionrolistes.fr/?webhook=https://discord.com/api/webhooks/875068900612665396/DJusy0eGs9Xyx2os-dodBVfWia2fbhfBzfmnDM9g-30ozoFYAuZBHVXaD9TKaC1wwBwg", description="⬆️ Here is the link to create your presentation.", title="Union Roliste - Presentation", color= 0x0CC1EE)
    embed.set_author(name=event.author.display_name, icon_url=event.author.avatar_url)

    DATA = ["**:pen_ballpoint:  Nom\n**","**:pen_ballpoint:  Prenom\n**",":round_pushpin:  **Address\n**",":telephone:   **N° Telephone\n**", ":postbox: **Code postal\n**","**:computer:  Support (Windows / Linux / Mac)\n**","**Expérience en programmation\n**"]
    embed.add_field(name="**\n**", value="**───────────────────────────────**", inline=False)

    embed.set_footer(text="Union Roliste dev presentation.", icon_url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4")

    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4")

    await event.author.send(embed=embed) # envoie un message de presentation privée à l'auteur qui a fait a commandes

async def on_help(event,*args):
    embed = discord.Embed(title="URBOT - helper", color= 0x0CC1EE) 
    embed.set_author(name="UR-BOT", icon_url="https://cdn.discordapp.com/avatars/1040275175687606372/33d5a8782c1d658caeeae59799e722b0.webp?size=32")
    
    HELP = str(f"**prefix :    {BOT_PREFIX}**\n\n\t```diff\n")
    for x in HELP_DATA.items():
            HELP += f"\r+ {x[0]}\n\n\t"
            c = GetMaxStrSizeInArray(x[1].items(),lambda a : a[1]['cmd'].__len__()) # Obtenir la chaine la plus longe pour ensuite center la fleche (->)
            for cmd in x[1].items():
                _offset = (c - cmd[1]["cmd"].__len__())+1 # centrage de lq flèche (->)
                HELP += cmd[1]["cmd"]+ (" "*_offset) + "-> "+cmd[1]["help"]+"\n\t" # Ecrit la command -> description

    HELP += f"\n```"

    embed.add_field(name="**\n**", value="**───────────────────────────────**", inline=False)

    embed.add_field(name="**\n**", value=HELP, inline=False)

    embed.set_footer(text="Union Roliste commands helper.", icon_url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4")

    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4") # set le logo en haut a droit

    await event.channel.send(embed=embed);
