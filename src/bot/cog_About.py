from discord.ext import commands
import templates
from bot import _, strings
import urpy
from urpy.utils import *

class About(commands.Cog):
    """ This cog contains commands used to get general information about the bot. """
    __doc__ = strings.About_descr

    def __init__(self, owner: urpy.MyBot):
        """ Creates an about cog. """
        super(About, self).__init__()
        self.bot = owner

    @commands.command(brief=strings.version_brief, help=strings.version_help)
    async def version(self, ctx: commands.Context):
        """ Displays the version numbers. """
        await self.send_info_msg(ctx)

    @commands.command(brief=strings.credit_brief, help=strings.credit_help)
    async def credit(self, ctx: commands.Context):
        """ Displays the credits. """
        await self.send_info_msg(ctx, with_credits=True)

    async def send_info_msg(self, ctx, with_credits=False):
        """ Sends a message containing the names, version numbers [and credits] of all the services. """
        # generates the descriptions for all the subservices of the bot
        services = "\n\n".join(
            formatted_template(templates, 'service_template.txt',
                               name=cog.get_name(),
                               version=cog.get_version(),
                               credits=cog.get_credits() if with_credits else "")

            for name, cog in self.bot.cogs.items() if isinstance(cog, urpy.MyCog)
        )

        # sends the message
        await ctx.send(code_block(formatted_template(templates, 'version_template.txt',
                                                     version=self.bot.get_version(),
                                                     name=self.bot.get_name(),
                                                     services=services,
                                                     credits=self.bot.get_credits() if with_credits else "")))
