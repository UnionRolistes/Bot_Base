import gettext
from discord.ext import commands
from Bot_Base.src.urpy.localization import Localization
from Bot_Base.src.urpy.my_commands import MyBot
from Bot_Base.src.urpy.utils import colored_message, SUCCESS_COLOR, ERROR_COLOR
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
    __doc__ = strings.GENERAL_DESCR

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

    @commands.command(brief=strings.EDIT_BRIEF, help=strings.EDIT_HELP)
    async def edit(self, ctx):
        """Call callbacks bound to the edit command."""
        await self.call_callbacks('edit', ctx)

    @commands.command(brief=strings.DONE_BRIEF, help=strings.DONE_HELP)
    async def done(self, ctx):
        """Call callbacks bound to the done command."""
        await self.call_callbacks('done', ctx)

    @commands.command(brief=strings.CANCEL_BRIEF)
    async def cancel(self, ctx):
        """Call callbacks bound to the cancel command."""
        await self.call_callbacks('cancel', ctx)

    @commands.command(brief=strings.LANG_BRIEF, help=strings.LANG_HELP)
    async def lang(self, ctx: commands.Context, language):
        """Switches to specified language"""
        if self.localization.set_user_language(ctx.author.id):
            await ctx.send(colored_message(
                _("Your language has successfully been set to {language}!").format(language=language),
                SUCCESS_COLOR))
        else:
            await ctx.send(colored_message(_("Sorry, I don't know this language!"), ERROR_COLOR))

    def add_to_command(self, command: str, *callbacks):
        """Adds a callback to the specified command. It will be called on command invocation."""
        for callback in callbacks:
            self.callbacks[command].append(callback)
