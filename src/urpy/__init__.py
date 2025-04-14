from Bot_Base.src.urpy.localization import Localization, lcl
from Bot_Base.src.urpy.help import MyHelpCommand
from Bot_Base.src.urpy.my_commands import MyBot, MyCog, MyContext
from Bot_Base.src.urpy.get_ressources import *

base_localization = Localization('../locale')  # TODO path for linux
_ = base_localization.gettext
