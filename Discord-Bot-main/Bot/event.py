
import asyncio
import discord

BOT_PREFIX   = "*"
BOT_VERSION  = "1.0.0"



def GetMaxCommandSize(array:dict):

    CmdData = {"size":0,"type":{}}

    for cmd in array:

        if(cmd.description and cmd.description != ""):
            CmdData["type"][cmd.description] = []

        if(cmd.name and cmd.help):
           _r = (cmd.name+(" ("+",".join(cmd.aliases)+") " if (cmd.aliases!=[]) else "")).__len__();
        if(_r > CmdData["size"]):
           CmdData["size"] = _r

    return CmdData


async def on_ping(event,bot_instance):
         await asyncio.gather(  # concurent await
            event.message.add_reaction('🏓'),
            event.send('Pong! 🏓 {0} ms'.format(
                round(bot_instance.latency, 3) * 1000))
        )

        

async def on_message(event,*args,**kwargs):
    if event.content.startswith('hi'):
        await event.channel.send(f'Hello! Mis a jour : {args}')

async def on_prez(event,*args,**kwargs):
    embed = discord.Embed(url="http://presentation.unionrolistes.fr/?webhook=https://discord.com/api/webhooks/875068900612665396/DJusy0eGs9Xyx2os-dodBVfWia2fbhfBzfmnDM9g-30ozoFYAuZBHVXaD9TKaC1wwBwg", description="⬆️ Here is the link to create your presentation.", title="Union Roliste - Presentation", color= 0x0CC1EE)
    embed.set_author(name=event.author.display_name, icon_url=event.author.avatar_url)
    embed.add_field(name="**\n**", value="**───────────────────────────────**", inline=False)
    embed.set_footer(text="Union Roliste dev presentation.", icon_url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4")
    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/62179928?s=200&v=4")

    await event.author.send(embed=embed) # envoie un message de presentation privée à l'auteur qui a fait a commandes


async def on_help(event,bot_instance,*args):

    HELP = str(f"```diff\n\nprefix : {BOT_PREFIX}\n\n")

    c = GetMaxCommandSize(bot_instance.walk_commands()) # Obtenir la chaine la plus longe pour ensuite center la fleche (->)

    for command in bot_instance.walk_commands(): # pour chaque commandes
        
        fullcmd = (command.name+(" ("+",".join(command.aliases)+") " if (command.aliases!=[]) else "" ))  

        _offset = (c["size"] - fullcmd.__len__())+1 # centrage de la flèche (->)

      
        if(command.name and command.help):
            fullcmd +=  (" "*_offset) + "-> "+command.help 
            if(command.description in [*c["type"].keys()]):
                c["type"][command.description].append(fullcmd) # Ajout la command à la description actuel (About, Presentation, No Category)
              
    for category in c["type"]: # prépare le text final qui sera afficher
        HELP += category+":" # ajout la cqtégory
        for help in c["type"][category]: # pour chaque command dans la catégory qlors on l'ajout au text final (HELP)
            HELP += "\n"+"\t"+help
        HELP += "\n\n";
     

    HELP += f"Entrez $help commande pour plus d'info sur une commande.\nVous pouvez aussi entrer $help categorie pour plus d'info sur une catégorie.```"

    await event.channel.send(HELP); 
