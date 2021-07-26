from urpy.localization import Localization, lcl
from urpy.help import MyHelpCommand
from urpy.my_commands import MyBot, MyCog, MyContext
from urpy.get_ressources import *

base_localization = Localization('../locale')  # TODO path for linux
_ = base_localization.gettext
