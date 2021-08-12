import discord
from discord.ext import commands

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com

from urpy.localization import lcl

_ = lcl


class MyHelpCommand(commands.DefaultHelpCommand):
    def __init__(self, localization, **options):
        super().__init__(
            help=lcl('Shows this message'),
            commands_heading=lcl('Commands:'),
            no_category=lcl('No Category'), **options)  # TODO 'No Category' in french
        global _
        # This check is necessary cause HelpCommand is deep copied every time in discord api. """
        if _ is lcl:
            _ = localization.gettext

    def add_command_formatting(self, command):
        """A utility function to format the non-indented block of commands and groups.

        Parameters
        ------------
        command: :class:`Command`
            The command to format.
        """

        if command.description:
            self.paginator.add_line(_(command.description), empty=True)

        signature = self.get_command_signature(command)
        self.paginator.add_line(signature, empty=True)
        domain = getattr(command.cog, 'domain', None)
        if command.help:
            try:
                self.paginator.add_line(_(command.help, domain), empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(line)  # TODO localization here
                self.paginator.add_line()

    def get_ending_note(self):
        """:class:`str`: Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        command_name = self.invoked_with
        return _("Type {0}{1} command for more info on a command.\n"
                 "You can also type {0}{1} category for more info on a category.").format(self.clean_prefix,
                                                                                          command_name)

    def add_indented_commands(self, commands, *, heading, max_size=None):
        if not commands:
            return
        if heading.startswith('\u200b'):
            heading = _(heading[1:-1]) + ':'
        self.paginator.add_line(_(heading[:-1]) + heading[-1])
        max_size = max_size or self.get_max_size(commands)

        get_width = discord.utils._string_width
        for command in commands:
            domain = getattr(command.cog, 'domain', None)
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = '{0}{1:<{width}} {2}'.format(self.indent * ' ', name, _(command.short_doc, domain), width=width)
            self.paginator.add_line(self.shorten_text(entry))

    async def send_cog_help(self, cog):
        domain = getattr(cog, 'domain', None)
        if cog.description:
            self.paginator.add_line(_(cog.description, domain), empty=True)
        filtered = await self.filter_commands(cog.get_commands(), sort=self.sort_commands)
        self.add_indented_commands(filtered, heading=_(self.commands_heading, domain))

        note = self.get_ending_note()
        if note:
            self.paginator.add_line()
            self.paginator.add_line(note)

        await self.send_pages()
