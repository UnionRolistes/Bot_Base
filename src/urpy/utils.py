import re
import sys
from importlib import resources

import discord
import requests


# UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# Ask a derogation at Contact.unionrolistes@gmail.com

def error_log(*msg, name="BOT"):
    print(f"{name}:ERROR|", *msg, file=sys.stderr)


async def get_public_ip() -> str:
    """
    Return public IP.

    @author Lyss
    @mail <delpratflo@cy-tech.fr>
    @date 28/06/21


    Returns
    -------
        str
            IP address.
    """
    return requests.get('https://api.ipify.org').text


async def get_informations(msg: discord.Message):
    """
    Extract information from an announcement message.

    @author Lyss
    @mail <delpratflo@cy-tech.fr>
    @date 28/06/21

    Parameters
    ----------
        msg : str
            Announcement message.

    Returns
    -------
        dict[str, str]
            A dict linking an information name to its value.
            Ex: " ** Type ** One Shoot  " becomes {'type': 'One Shoot'}
    """
    infos = {}

    # Matches strings of the form : ' ** {name} **  {value} ' ending on ':', '**' or '\n'
    for match in re.finditer(" \\*\\*(.*)\\*\\* *(?:\n|)(.*)\n(?::|\\*\\*|\n)", msg.embeds[0].description):
        infos[match.group(1).strip().lower()] = match.group(2)
    return infos


# Couleurs "dim" (2;3x) rendues par le client Discord dans un code block ```ansi.
HEADING_COLOR = '\x1b[2;34;4m'  # bleu, souligne
COMMAND_COLOR = '\x1b[2;33m'  # jaune
DESCRIPTION_COLOR = '\x1b[2;36m'  # cyan
SUCCESS_COLOR = '\x1b[2;32m'  # vert
ERROR_COLOR = '\x1b[2;31m'  # rouge
RESET_COLOR = '\x1b[0m'


def code_block(s):
    return f"```{s}```"


def ansi_block(s):
    return f"```ansi\n{s}```"


def colorize(s, color=DESCRIPTION_COLOR):
    return f'{color}{s}{RESET_COLOR}'


def colored_message(s, color=SUCCESS_COLOR):
    """Wraps a plain bot message in a colored ```ansi code block."""
    return ansi_block(colorize(s, color))


def edit_fmt(s):
    return f"\\|~ {s} ~|"


def code_line(s: str):
    return f"`{s}`"


def formatted_template(template_pckg, template_name, **kwargs):
    res = ""
    size_last_line = 0
    with resources.open_text(template_pckg, template_name) as f:
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
                formatted = match.group(5).format(**kwargs)
                # une valeur substituee (ex: credits multi-auteurs) peut contenir plusieurs
                # lignes ; sans reappliquer l'indentation de la ligne du template a chacune
                # d'elles, seule la premiere serait indentee. Le saut de ligne final de la
                # ligne elle-meme (pas celui d'une valeur substituee) est laisse de cote pour
                # ne pas indenter ce qui suit sur la ligne suivante du template.
                indent = match.group(1)
                if '\n' in formatted:
                    has_trailing_newline = formatted.endswith('\n')
                    body = formatted[:-1] if has_trailing_newline else formatted
                    formatted = body.replace('\n', '\n' + indent) + ('\n' if has_trailing_newline else '')
                new_line += formatted

            size_last_line = len(new_line.strip())

            if size_last_line or (not size_last_line and not match.group(6)):
                res += new_line

    if res.endswith('\n'):
        return res[:-1]
    else:
        return res


def log(*msgs, name='BOT'):
    print(f"{name}|", *msgs, file=sys.stderr)


def html_header_content_type(*msgs):
    print("Content-Type: text/html")
    print()
    print(*msgs, sep='\n')


def html_header_relocate(dest: str):
    print("Status: 303 See other")
    print(f"Location: {dest}")
    print()


def html_header_webhook_not_supplied():
    html_header_content_type('Error: Webhook not supplied.')
