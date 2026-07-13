import discord
from discord.ext import commands

# UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# Ask a derogation at Contact.unionrolistes@gmail.com

from Bot_Base.src.urpy.localization import lcl
from Bot_Base.src.urpy.utils import HEADING_COLOR, COMMAND_COLOR, DESCRIPTION_COLOR, RESET_COLOR

_ = lcl


class MyHelpCommand(commands.DefaultHelpCommand):
    def __init__(self, localization, **options):
        super().__init__(
            help=lcl('Shows this message'),
            commands_heading=lcl('Commands:'),
            no_category=lcl('No Category'),  # TODO 'No Category' in french
            paginator=commands.Paginator(prefix='```ansi', suffix='```'),
            **options)
        global _
        # This check is necessary cause HelpCommand is deeply copied every time in discord api. """
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
            self.paginator.add_line(f'{DESCRIPTION_COLOR}{_(command.description)}{RESET_COLOR}', empty=True)

        signature = self.get_command_signature(command)
        self.paginator.add_line(f'{COMMAND_COLOR}{signature}{RESET_COLOR}', empty=True)
        # 'domain = getattr(command.cog, 'domain', None)' ; la variable n'est jamais utilisée. À laisser au cas où ça
        # servirait un futur développeur.
        if command.help:
            try:
                self.paginator.add_line(f'{DESCRIPTION_COLOR}{_(command.help)}{RESET_COLOR}', empty=True)
            except RuntimeError:
                self.paginator.add_line(DESCRIPTION_COLOR)
                for line in command.help.splitlines():
                    self.paginator.add_line(line)  # TODO localization here
                self.paginator.add_line(RESET_COLOR)

    def get_ending_note(self):
        """:class:`str`: Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        command_name = self.invoked_with
        note = _(f"Type {self.clean_prefix}{command_name} command for more info on a command.\n"
                 f"You can also type {self.clean_prefix}{command_name} category for more info on a category.")
        return f'{DESCRIPTION_COLOR}{note}{RESET_COLOR}'
        # Une erreur se produit sur 'self.clean_prefix'.
        # En effet, l'IDE demande la création de cette méthode dans la classe.

    def add_indented_commands(self, instructions, *, heading, max_size=None):
        if not instructions:
            return
        if heading.startswith('\u200b'):
            heading = _(heading[1:-1]) + ':'
        self.paginator.add_line(f'{HEADING_COLOR}{_(heading[:-1])}{RESET_COLOR}{heading[-1]}')
        max_size = max_size or self.get_max_size(instructions)

        get_width = discord.utils._string_width  # Erreur : 'Access to a protected member _string_width of a module'.
        for command in instructions:
            # domain = getattr(command.cog, 'domain', None) ; la variable n'est jamais utilisée. À laisser au cas où ça
            # servirait un futur développeur.
            name = command.name
            width = max_size - (get_width(name) - len(name))
            # le padding se calcule sur le nom brut : les codes ANSI ajoutes ensuite ne comptent pas
            # dans la largeur visible, mais fausseraient l'alignement s'ils etaient inclus dans le format.
            padded_name = '{0:<{width}}'.format(name, width=width)
            entry = '{0}{1}{2}{3} {4}{5}{6}'.format(
                self.indent * ' ', COMMAND_COLOR, padded_name, RESET_COLOR,
                DESCRIPTION_COLOR, _(command.short_doc), RESET_COLOR)
            self.paginator.add_line(self.shorten_text(entry))

    async def send_cog_help(self, cog):
        # 'domain = getattr(cog, 'domain', None)' ; la variable n'est jamais utilisée. À laisser au cas où ça
        # servirait un futur développeur.
        if cog.description:
            self.paginator.add_line(f'{DESCRIPTION_COLOR}{_(cog.description)}{RESET_COLOR}', empty=True)
        filtered = await self.filter_commands(cog.get_commands(), sort=self.sort_commands)
        self.add_indented_commands(filtered, heading=_(self.commands_heading))

        note = self.get_ending_note()
        if note:
            self.paginator.add_line()
            self.paginator.add_line(note)

        await self.send_pages()
