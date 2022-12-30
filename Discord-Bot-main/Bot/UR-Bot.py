import discord
from dotenv import load_dotenv
import event
from discord.ext import commands
import sys
import os



load_dotenv()
TOKEN = os.getenv('TOKEN')

class UR_BOT(commands.Bot):

    Commands =  dict();

    async def on_ready(self):
        print('--- We have successfully loggged in as {0.user}'.format(self))
    

    async def on_message(self, message):

        if message.author == self.user:
               return
        
        await event.on_message(message,bot_instance=bot);

        return await bot.process_commands(message)
   

    

intent = discord.Intents.default()
intent.members = True
intent.messages = True

bot = UR_BOT(command_prefix= event.BOT_PREFIX,intents=intent)
bot.remove_command("help")


@bot.command(name="ping",help="Renvoi un pong",description="No Category")
@commands.guild_only()
async def ping(ctx):
    await  event.on_ping(ctx,bot_instance=bot)




@bot.command(name="help", help="Affiche les commandes disponible",description="No Category",aliases=['h'])
async def help(ctx):
     await event.on_help(ctx,bot_instance=bot)

@bot.command(name="prez", help="Envoie un lien pour se présenter",description="Presentation")
async def prez(ctx):
  await event.on_prez(ctx,bot_instance=bot)


@bot.command(name="credits", help='affiche les credits', aliases=['c'], description="About" )
async def _credits(ctx):
  credits = "```properties\n"
  credits += (open((sys.path[0]+"/credits.txt"),mode="r")).read()
  await ctx.send(credits+'```')


@bot.command(name="version", help='affiche les credits', aliases=['v'], description="About" )
async def _version(ctx):
  bot_version =  "```properties\n Bot version : "
  bot_version += event.BOT_VERSION
  await ctx.send(bot_version+'```')


bot.run(TOKEN)

