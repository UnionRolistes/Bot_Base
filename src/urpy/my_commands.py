from functools import partial
from types import MethodType

import discord
from discord.ext import commands
from importlib import resources
from abc import ABC, abstractmethod, ABCMeta

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com

class VersionNCreditInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_credits():
        """ Return credits. """
        pass

    @staticmethod
    @abstractmethod
    def get_version() -> str:
        """ Return version number."""
        pass

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """ Return name."""
        pass


class MyBot(commands.Bot, VersionNCreditInterface):
    @abstractmethod
    def __init__(self, command_prefix='$', *args, **kwargs):
        super(MyBot, self).__init__(command_prefix=command_prefix, *args, **kwargs)

class MyCogMeta(type(commands.Cog), VersionNCreditInterface, ABCMeta):
    pass

# TODO: shaky code, needs to be cleaned
class MyCog(commands.Cog, VersionNCreditInterface, metaclass=MyCogMeta):
    def __init__(self, bot, domain):
        self.bot = bot
        self.domain = domain

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\t| {self.qualified_name} started.")

# TODO: à améliorer
from functools import wraps


# def add_to_comm(name):
#     def decorator(method):
#         @wraps(method)
#         def _impl(self, *method_args, **method_kwargs):
#             print(str(method))
#         return _impl
#
#     return decorator


    # args[0].bot.add_to_command(name, partial(func, args[0]))
#
# class Test:
#     def __init__(self, name):
#         self.name = name
#
#     @add_to_comm("non")
#     def test(self):
#         print("doggo")
#
#     @add_to_comm("yes")
#     def toost(self):
#         print("cat")
#
# t = Test("Alpha")
# # t.test()
# # t.toost()

class MyContext(commands.Context):
    def __init__(self, ctx: commands.Context, delete_after=None):
        """
        Creates a Context whose messages sent are deleted by default.

        @author Lyss
        @mail <delpratflo@cy-tech.fr>
        @date 28/06/21

        Parameters
        ----------
        ctx : context to copy
        """
        super().__init__(**ctx.__dict__)
        self.delete_after = delete_after

    async def send(self, content=None, **kwargs):
        """
        Override Context.send to delete messages by default.

        @author Lyss
        @mail <delpratflo@cy-tech.fr>
        @date 28/06/21

        Parameters
        ----------
        content
        kwargs

        Returns
        -------

        """
        if 'delete_after' not in kwargs:
            kwargs['delete_after'] = self.delete_after

        await self.message.delete(delay=kwargs['delete_after'])
        await super().send(content, **kwargs)
