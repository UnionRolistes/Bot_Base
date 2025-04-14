"""
Ce module contient les chaînes de caractères utilisées pour les messages
et les descriptions envoyés par le bot Discord.
"""

from Bot_Base.src.urpy.localization import lcl

BOT_TITLE = lcl('URbot - The discord bot of "l\'Union des Rôlistes"')
LANG_BRIEF = lcl('Switches to specified language')
LANG_HELP = lcl(
    """\
Switches to specified language

Available languages :
    - en
    - fr
    - special-rp\
""")
DONE_BRIEF = lcl('Confirms the current action')
DONE_HELP = LANG_BRIEF
EDIT_BRIEF = lcl('Edits a message')
EDIT_HELP = EDIT_BRIEF
CANCEL_BRIEF = lcl('Cancels the current action')
CANCEL_HELP = CANCEL_BRIEF
VERSION_BRIEF = lcl('Displays the version numbers')
VERSION_HELP = VERSION_BRIEF
CREDIT_BRIEF = lcl('Displays the credits')
CREDIT_HELP = CREDIT_BRIEF
ABOUT_DESCR = lcl('This category groups various commands to display general information about the bot.')
GENERAL_DESCR = lcl('This category groups various commands whose utility depends on the context.')
