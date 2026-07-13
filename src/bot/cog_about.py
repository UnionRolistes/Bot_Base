from discord.ext import commands
from Bot_Base.src.bot import templates
from Bot_Base.src.urpy.my_commands import MyBot, MyCog
from Bot_Base.src.urpy.utils import *
import strings


# UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# Ask a derogation at Contact.unionrolistes@gmail.com

class About(commands.Cog):
    """ This cog contains commands used to get general information about the bot. """
    __doc__ = strings.ABOUT_DESCR

    def __init__(self, owner: MyBot):
        """ Creates an 'about cog'. """
        super(About, self).__init__()
        self.bot = owner

    @commands.command(brief=strings.VERSION_BRIEF, help=strings.VERSION_HELP)
    async def version(self, ctx: commands.Context):
        """ Displays the version numbers. """
        await self.send_info_msg(ctx)

    @commands.command(brief=strings.CREDIT_BRIEF, help=strings.CREDIT_HELP)
    async def credit(self, ctx: commands.Context):
        """ Displays the credits. """
        await self.send_info_msg(ctx, with_credits=True)

    async def send_info_msg(self, ctx, with_credits=False):
        """ Sends a message containing the names, version numbers [and credits] of all the services. """
        # generates the descriptions for all the subservices of the bot
        services = "\n\n".join(
            formatted_template(templates, 'service_template.txt',
                               name=cog.get_name(),
                               version=colorize(cog.get_version(), COMMAND_COLOR),
                               credits=colorize(cog.get_credits(), DESCRIPTION_COLOR) if with_credits else "")

            for name, cog in self.bot.cogs.items() if isinstance(cog, MyCog)
        )

        # sends the message. Le nom du bot et des services reste non colore : le padding des
        # soulignements '====='/'-----' de formatted_template se calcule sur ces lignes, et des
        # codes ANSI y fausseraient la longueur visible.
        await ctx.send(ansi_block(formatted_template(templates, 'version_template.txt',
                                                     version=colorize(self.bot.get_version(), COMMAND_COLOR),
                                                     name=self.bot.get_name(),
                                                     services=services,
                                                     credits=colorize(self.bot.get_credits(), DESCRIPTION_COLOR) if with_credits else "")))
