import re
import sys
import requests
import discord
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

async def get_informations(msg: discord.Message) -> dict[str, str]:
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