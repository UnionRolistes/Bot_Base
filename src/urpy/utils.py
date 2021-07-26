import re
import sys
import requests
import discord
from importlib import resources

def error_log(*msg, name="BOT"):
    print(f"{name}: ERROR | ", *msg, file=sys.stderr)


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
    for match in re.finditer("\*\*(.*)\*\* *(?:\n| )(.*)\n(?::|\*\*|\n)", msg.embeds[0].description):
        infos[match.group(1).strip().lower()] = match.group(2)
    return infos


def code_block(s):
    return f"```{s}```"

def edit_fmt(s):
    return f"\|~ {s} ~|"

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
                new_line += match.group(5).format(**kwargs)

            size_last_line = len(new_line.strip())

            if size_last_line or (not size_last_line and not match.group(6)):
                res += new_line

    if res.endswith('\n'):
        return res[:-1]
    else:
        return res