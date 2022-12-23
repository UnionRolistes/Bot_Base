# ext import
import discord
from dotenv import load_dotenv
# import DebugBot
from discord.ext import commands
import os
import asyncio

# load .env file
load_dotenv()

# get token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')  # get token from .env file
BOT_PREFIX = os.getenv('BOT_PREFIX')  # get prefix from .env file

# exit if no token found
if TOKEN is None:
    print("The discord token is not defined \n\t defined it in the .env file (dev) \n\t or in the environment in docker-compose")
    exit(1)


class BOT_BASE(commands.Bot):
    async def on_ready(self):
        print('--- We have successfully loggged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return
        return await bot.process_commands(message)


# set listeners
intent = discord.Intents.default()
intent.members = True
intent.messages = True
intent.message_content = True  # v2

bot = BOT_BASE(command_prefix=BOT_PREFIX, intents=intent)  # build bot

groups = {}

# laod all extensions in the glob "./**/*.py"
# like that to limit side effect between extension


async def load_all_extensions():
    for dir in os.listdir('./extends'):
        # run pip install -r requirements.txt if exists
        if os.path.exists('./extends/'+dir+'/requirements.txt'):
            try:
                print('pip install -r ./extends/'+dir+'/requirements.txt')
                os.system('pip install -r ./extends/'+dir+'/requirements.txt')
            except:
                print('pip install -r ./extends/' +
                      dir+'/requirements.txt failed')
        for file in os.listdir('./extends/'+dir):
            if file.endswith('.py'):
                try:
                    print(dir+'/'+file)
                    await bot.load_extension('extends.'+dir+'.'+file[:-3])
                except Exception as e:
                    print('Failed to load extension {0}.'.format(file))
                    print(e)


# if the file is run directly, run the bot
if __name__ == '__main__':
    # load all extensions
    asyncio.run(load_all_extensions())

    # run bot
    bot.run(TOKEN)
