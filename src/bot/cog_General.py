import discord
from discord.ext import commands
import urpy

class General(commands.Cog):
    def __init__(self, URBot: urpy.MyBot):
        self.bot = URBot
        self.callbacks: dict[str, list] = {
            'edit': [],
            'done': [],
            'cancel': []
        }

    async def call_callbacks(self, command: str, ctx: commands.Context):
        for callback in self.callbacks[command]:
            await callback(ctx)

    @commands.command()
    async def edit(self, ctx):
        """ Édite un message """
        await self.call_callbacks('edit', ctx)

    @commands.command()
    async def done(self, ctx):
        """ Confirme l'action en cours"""
        await self.call_callbacks('done', ctx)

    @commands.command()
    async def cancel(self, ctx):
        """ Annule l'action en cours """
        await self.call_callbacks('cancel', ctx)

    def add_to_command(self, command: str, *callbacks):
        for callback in callbacks:
            self.callbacks[command].append(callback)
