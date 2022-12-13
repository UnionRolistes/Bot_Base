import discord
from dotenv import load_dotenv
import DebugBot
from discord.ext import commands
import os



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN', None)
if TOKEN is None:
    print("The discord token is not defined \n\t defined it in the .env file (dev) \n\t or in the environment in docker-compose")
    exit(1)

class UR_BOT(commands.Bot):

    async def on_ready(self):
        print('--- We have successfully loggged in as {0.user}'.format(self))

    async def on_message(self, message):

        if message.author == self.user:
               return

        await DebugBot.debug_on_message(message);

        return await bot.process_commands(message)




intent = discord.Intents.default()
intent.members = True
intent.messages = True

bot = UR_BOT(command_prefix= DebugBot.event.BOT_PREFIX,intents=intent)
bot.remove_command('help')



@bot.command(name="ping")
@commands.guild_only()
async def ping(ctx):
    await  DebugBot.debug_on_ping(ctx)




@bot.command(name="help")
async def help(ctx):
     await DebugBot.debug_on_help(ctx)

@bot.command(name="prez")
async def prez(ctx):
  await DebugBot.debug_on_prez(ctx)


@DebugBot.update_all_modules
async def reload_module():
    return 0;



@bot.command(aliases=['reload', 'rld'])
async def reload_module(ctx):
    await reload_module();
    await ctx.channel.send("The scripts has been reloaded.");
    return 0;


bot.run(TOKEN)
