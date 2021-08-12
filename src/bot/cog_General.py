from discord.ext import commands
import bot
from bot import localization, _, strings
import urpy

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com


class General(commands.Cog):
    __doc__ = strings.General_descr

    def __init__(self, URBot: urpy.MyBot):
        self.bot = URBot
        self.callbacks = {
            'edit': [],
            'done': [],
            'cancel': []
        }

    async def call_callbacks(self, command: str, ctx: commands.Context):
        for callback in self.callbacks[command]:
            await callback(ctx)

    @commands.command(brief=strings.edit_brief, help=strings.edit_help)
    async def edit(self, ctx):
        """ Call callbacks bound to the edit command. """
        await self.call_callbacks('edit', ctx)

    @commands.command(brief=strings.done_brief, help=strings.done_help)
    async def done(self, ctx):
        """ Call callbacks bound to the done command. """
        await self.call_callbacks('done', ctx)

    @commands.command(brief=strings.cancel_brief)
    async def cancel(self, ctx):
        """ Call callbacks bound to the cancel command. """
        await self.call_callbacks('cancel', ctx)

    @commands.command(brief=strings.lang_brief, help=strings.lang_help)
    async def lang(self, ctx: commands.Context, language):
        """ Switches to specified language """
        if language in localization.languages:
            localization.set_user_language(language)
            await ctx.send(_("Your language has successfully been set to english !"))

        else:
            await ctx.send(_("Sorry, i don't know this language !"))

    def add_to_command(self, command: str, *callbacks):
        """ Adds a callback to the specified command. It will be called on command invokation."""
        for callback in callbacks:
            self.callbacks[command].append(callback)
