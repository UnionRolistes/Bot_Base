
from Bot_Base.src.urpy.localization import Localization

import platform

if platform.system() == 'Windows':
    localedir = '../locale'
else:
    localedir = '/usr/local/bin/URbot/locale'

localization = Localization()
domain = 'bot_base'
# TODO automate adding all languages
localization.set_localedir(localedir)
localization.add_translation('bot_base', ['fr'])
localization.add_translation('bot_base', ['en'])
localization.add_translation('bot_base', ['special-rp', 'fr'])


_ = localization.gettext
