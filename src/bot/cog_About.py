import re
import sys
from importlib import resources

from discord.ext import commands
import template

class About(commands.Cog):
    def __init__(self, owner_bot):
        super(About, self).__init__()
        self.bot = owner_bot

    @commands.command()
    async def version(self, ctx: commands.Context):
        """
        Affiche les numéros de versions
        """
        await self.send_info_msg(ctx)

    @commands.command()
    async def credit(self, ctx: commands.Context):
        """
        Affiche les crédits
        """
        await self.send_info_msg(ctx, with_credits=True)

    async def send_info_msg(self, ctx, with_credits=False):
        if with_credits:
            _credits = self.bot.get_credits()
        else:
            _credits = ""

        try:
            services = "\n\n".join(
                formatted_template('service_template.txt', name=cog.get_name(), version=cog.get_version(), credits=cog.get_credits() if with_credits else "")
                for name, cog in self.bot.cogs.items() if name != self.qualified_name)

        except AttributeError as e:
            print(f"Error: {e}\n\t| Les cogs doivent implémenter get_name, get_version and get_credit.", file=sys.stderr)
        else:
            await ctx.send("```" + formatted_template('version_template.txt', version=self.bot.get_version(), name=self.bot.get_name(), services=services, credits=_credits) + "```")


def formatted_template(template_name, **kwargs):
    res = ""
    size_last_line = 0
    with resources.open_text(template, template_name) as f:
        for line in f:
            # regex match to analyze the line -> the goal is to identify chars that indicate the position of
            # an underline such as === and --- (the ---- form doesn't accept anything after it, otherwise
            # it is not considered as an underline)
            match = re.match('([ \t]*)(?:(-+)([ \t\n]*$)|(=*)((?:({.*})|.)*))', line, flags=re.DOTALL | re.MULTILINE)
            new_line = match.group(1)

            # case of a --- underline
            if match.group(2):
                new_line += match.group(2)[0] * size_last_line
                new_line += match.group(3)
            else:
                # case of a === underline
                if match.group(4):
                    new_line += match.group(4)[0] * size_last_line
                # formats text that doesn't symbolize an underline
                new_line += match.group(5).format(**kwargs)

            size_last_line = len(new_line.strip())

            if size_last_line or (not size_last_line and not match.group(6)):
                res += new_line

    if res.endswith('\n'):
        return res[:-1]
    else:
        return res
