import os
import asyncio
from discord.ext import commands


class Base(commands.Cog, name='Base'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    # Chargement initial du Cog
    async def cog_load(self):
        print(f"{self.__class__.__name__} est chargée")

    # Commande de ping
    @commands.command(name="ping", help='ping pong avec le bot', aliases=['pong', 'p'])
    @commands.guild_only()
    async def _ping(self, ctx):
        await self._send_pong_response(ctx)

    # Commande d'affichage des crédits
    @commands.command(name="credentials", help='affiche les crédits', aliases=['credit', 'c'])
    async def _credits(self, ctx):
        credentials = await self._get_credits()
        if credentials:
            await ctx.send(credentials)
        else:
            await ctx.send("Aucune information de crédits disponible.")

    # Commande d'affichage des versions
    @commands.command(name="version", help='affiche la version du bot', aliases=['v'])
    async def _version(self, ctx):
        versions = await self._get_versions()
        if versions:
            await ctx.send(versions)
        else:
            await ctx.send("Aucune information de versions disponible.")

    # Commande d'aide
    @commands.command(name="help", help='affiche les commandes, alias et description', aliases=['h', '?'])
    async def _help(self, ctx):
        help_msg = await self._generate_help_message()
        await ctx.send(help_msg)

    # Envoie une réponse "Pong !" avec le temps de latence du bot
    async def _send_pong_response(self, ctx):
        latency = round(self.bot.latency, 3) * 1000
        await asyncio.gather(
            ctx.message.add_reaction('🏓'),
            ctx.send(f'Pong ! 🏓 {latency} ms')
        )

    # Récupère les informations de crédits depuis les fichiers
    @staticmethod
    async def _get_credits():
        credentials = ""
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for directory in os.listdir(parent_dir):
            credits_file_path = os.path.join(parent_dir, directory, 'credits.txt')
            if os.path.exists(credits_file_path):
                try:
                    with open(credits_file_path, 'r') as f:
                        credentials += f.read() + '\n\n'
                except Exception as e:
                    print(e)
        if credentials:
            credits_lines = credentials.splitlines()
            formatted_credits = (
                f"```ansi\n"
                f"\x1b[1;34m{credits_lines[0]}\x1b[0m\n"  # Titre en bleu foncé
                f"\x1b[1;32m{credits_lines[1]}\x1b[0m\n"  # Ligne en vert clair
            )
            for line in credits_lines[2:]:
                formatted_credits += f"\x1b[1;36m{line}\x1b[0m\n"  # Lignes en cyan clair
            formatted_credits += "```"
            return formatted_credits
        else:
            return None

    # Récupère les informations de versions depuis les fichiers
    @staticmethod
    async def _get_versions():
        versions = ""
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directory_names = {
            'base': 'Bot_Base',
            'prez': 'Bot_Presentation',
            'planning': 'Bot_Planning',
            'site': 'Web_Site'
        }
        for directory in directory_names:
            version_file_path = os.path.join(parent_dir, directory, 'version.txt')
            if os.path.exists(version_file_path):
                try:
                    with open(version_file_path, 'r') as f:
                        version = f.read().strip()
                    formatted_version = (
                        f"```ansi\n"
                        f"\x1b[1;34m{directory_names[directory]}\x1b[0m : \x1b[1;37mVersion \x1b[1;33m{version}\x1b[0m\n"
                        f"```"
                    )
                    versions += formatted_version
                except Exception as e:
                    print(e)
            else:
                formatted_version = (
                    f"```ansi\n"
                    f"\x1b[1;34m{directory_names[directory]}\x1b[0m : \x1b[1;31mVersion introuvable\x1b[0m\n"
                    f"```"
                )
                versions += formatted_version
        if versions:
            return versions
        else:
            return None

    # Génère un message d'aide avec les commandes triées par catégorie
    async def _generate_help_message(self):
        commands_by_category = self._get_commands_by_category()
        help_msg = (
            f"```ansi\n"
            f"\x1b[2;34;4mPréfixe\x1b[0m \x1b[2;31m{self.bot.command_prefix}\x1b[0m\n\n"
        )
        for cat in commands_by_category:
            category_commands = commands_by_category[cat]
            command_list = self._get_command_list(category_commands)
            help_msg += f"\x1b[2;34;4m{cat}\x1b[0m :\n{command_list}\n"
        help_msg += "```"
        return help_msg

    # Trie les commandes par catégorie
    def _get_commands_by_category(self):
        commands_by_category = {}
        for command in self.bot.walk_commands():
            if command.cog_name not in commands_by_category:
                commands_by_category[command.cog_name] = []
            commands_by_category[command.cog_name].append(command)
        return dict(sorted(commands_by_category.items()))

    # Génère la liste de commandes pour une catégorie
    def _get_command_list(self, instructions):
        command_list = ""
        for command in instructions:
            aliases = self._get_command_aliases(command)
            msg = f' -- \x1b[2;36m{command.help}\x1b[0m' if command.help is not None else ''
            command_list += f"\x1b[2;33m{command.name}\x1b[0m{aliases}{msg}\n"
        return command_list

    # Récupère les alias d'une commande
    @staticmethod
    def _get_command_aliases(command):
        return f'''{' ' + str(command.aliases).replace("'", "") if command.aliases != [] else ''}'''


# Fonction d'initialisation du Cog
async def setup(bot):
    bot.remove_command('help')
    await bot.add_cog(Base(bot))
