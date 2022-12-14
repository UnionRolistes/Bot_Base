#ext import
import discord
from dotenv import load_dotenv
# import DebugBot
from discord.ext import commands
import os
import asyncio

#local import
import event

class BOT_BASE(commands.Bot):

    async def on_ready(self):
        print('--- We have successfully loggged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
               return
        # await DebugBot.debug_on_message(message);
        return await bot.process_commands(message)

#set listeners
intent = discord.Intents.default()
intent.members = True
intent.messages = True
intent.message_content = True #v2

bot = BOT_BASE(command_prefix= event.BOT_PREFIX,intents=intent) #build bot
# bot.remove_command('help')

#load extension base
asyncio.run(bot.load_extension("extends.base.event"))

@bot.command(name="_help")
async def help(ctx):
     await event.on_help(ctx)

@bot.command(name="prez")
async def prez(ctx):
  await event.on_prez(ctx)

@bot.command(aliases=['reload', 'rld'])
async def reload_module(ctx):
    await reload_module()
    await ctx.channel.send("The scripts has been reloaded.")
    return 0

# if the file is run directly, run the bot
if __name__ == '__main__':
    #load token from env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN', None)

    # exit if no token found
    if TOKEN is None:
        print("The discord token is not defined \n\t defined it in the .env file (dev) \n\t or in the environment in docker-compose")
        exit(1)

    # run bot
    bot.run(TOKEN)
