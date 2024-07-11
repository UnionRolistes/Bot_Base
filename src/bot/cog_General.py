import gettext
from discord.ext import commands
from Bot_Base.src.urpy.localization import Localization
from Bot_Base.src.urpy.my_commands import MyBot
import strings

# UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA). To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# Ask a derogation at Contact.unionrolistes@gmail.com

# Configuration de gettext pour la traduction
gettext.bindtextdomain('bot_base', 'locales')
gettext.textdomain('bot_base')
_ = gettext.gettext


class General(commands.Cog):
    """Cog contenant des commandes générales pour le bot."""
    __doc__ = strings.General_descr

    def __init__(self, ur_bot: MyBot):
        """Initialise une instance spécifiée plus haut."""
        self.bot = ur_bot
        self.localization = Localization()
        self.callbacks = {
            'edit': [],
            'done': [],
            'cancel': []
        }

    async def call_callbacks(self, command: str, ctx: commands.Context):
        """Appelle-les callbacks liés à une commande spécifique."""
        for callback in self.callbacks[command]:
            await callback(ctx)

    @commands.command(brief=strings.edit_brief, help=strings.edit_help)
    async def edit(self, ctx):
        """Call callbacks bound to the edit command."""
        await self.call_callbacks('edit', ctx)

    @commands.command(brief=strings.done_brief, help=strings.done_help)
    async def done(self, ctx):
        """Call callbacks bound to the done command."""
        await self.call_callbacks('done', ctx)

    @commands.command(brief=strings.cancel_brief)
    async def cancel(self, ctx):
        """Call callbacks bound to the cancel command."""
        await self.call_callbacks('cancel', ctx)

    @commands.command(brief=strings.lang_brief, help=strings.lang_help)
    async def lang(self, ctx: commands.Context, language):
        """Switches to specified language"""
        if self.localization.set_user_language(ctx.author.id):
            await ctx.send(_("Your language has successfully been set to {language}!").format(language=language))
        else:
            await ctx.send(_("Sorry, I don't know this language!"))

    def add_to_command(self, command: str, *callbacks):
        """Adds a callback to the specified command. It will be called on command invocation."""
        for callback in callbacks:
            self.callbacks[command].append(callback)
