import asyncio
from discord.ext import commands

class Base(commands.Cog, name='base'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def cog_load(self): # called when the cog is loaded
        print(self.__class__.__name__ + " is loaded")

    @commands.command(name="ping", help='ping pong with the bot',aliases=['pong'], )
    @commands.guild_only()
    async def _ping(self, event):
        await asyncio.gather( # concurent await
            event.message.add_reaction('🏓'),
            event.author.send("pong")
        )

async def setup(bot):
    await bot.add_cog(Base(bot))