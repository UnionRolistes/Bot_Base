
import cgi
from pickle import load
import re
from datetime import datetime

from aiohttp import ClientSession
from discord import AllowedMentions, Embed, Webhook  # , AsyncWebhookAdapter
from lxml import etree as et

from Bot_Base.src.urpy.localization import lcl, Localization
from Bot_Base.src.urpy.utils import error_log, log


# UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# Ask a derogation at Contact.unionrolistes@gmail.com

GAME_TAG = 'partie'
TITLE_TAG = 'titre'
MAX_PLAYER_TAG = 'capacite'
MIN_PLAYER_TAG = 'minimum'
NB_JOINED_TAG = 'inscrits'
DATE_TAG = 'date'
TIME_TAG = 'heure'
LENGTH_TAG = 'duree'
TYPE_TAG = 'type'
MJ_TAG = 'mj'
SYSTEM_TAG = 'systeme'
MINORS_ALLOWED_TAG = 'pjMineur'
PLATFORMS_TAG = 'plateformes'
DETAILS_TAG = 'details'
LINK_TAG = 'lien'

TAGS = [TITLE_TAG, MAX_PLAYER_TAG, MIN_PLAYER_TAG, NB_JOINED_TAG,
        DATE_TAG, TIME_TAG, LENGTH_TAG, TYPE_TAG, MJ_TAG, SYSTEM_TAG,
        MINORS_ALLOWED_TAG, PLATFORMS_TAG, DETAILS_TAG, LINK_TAG]

TAGS_TO_FORM = {
    TITLE_TAG: 'jdr_title',
    MAX_PLAYER_TAG: 'maxJoueurs',
    MIN_PLAYER_TAG: 'minJoueurs',
    # date_tag: 'jdr_date', car on ne veut pas que celui-là s'écrive automatiquement. ↓
    # On veut d'abord séparer la date et l'heure et faire le mettre sous la forme Y-M-D
    LENGTH_TAG: 'jdr_length',
    TYPE_TAG: 'jdr_type',
    SYSTEM_TAG: 'jdr_system',
    MINORS_ALLOWED_TAG: 'jdr_pj',
    DETAILS_TAG: 'jdr_details',
}

TAGS_TO_LAMBDA = {
    NB_JOINED_TAG: lambda f: '0',
    # time_tag: lambda f: '15h00',
    MJ_TAG: lambda f: f"&lt;@{f.getvalue('user_id')}&gt; [{f.getvalue('pseudo')}]",
    PLATFORMS_TAG: lambda f: " ".join(f.getlist('platform')),
    LINK_TAG: lambda f: 'https://discord.com/channels/TODO'
}

_ = lcl


class Calendar:
    """
    This class allows updating a xml file that contains the data of an event calendar.
    """
    creators_to_webhook = {}

    def __init__(self, fp: str, localization: Localization = None):  # TODO localization
        """
        Create an xmlCalendar.

        @fp path to xml file
        """
        self.fp = fp
        # import os
        # from Bot_Base.src.urpy import utils
        # utils.html_header_content_type()
        # print(os.listdir("/usr/share/urbot/"))
        # print(open("/usr/share"))
        self.tree: et.ElementTree = et.parse(self.fp, et.XMLParser(remove_blank_text=True))
        if localization is not None:
            global _
            _ = localization.gettext

    def get_last_id(self) -> int:  # TODO change name and more
        root = self.tree.getroot()

        if 'last_id' in root.attrib:
            return int(root.get('last_id'))
        else:
            last_id = self.find_last_id()
            root.set('last_id', str(last_id))
            return last_id

    def find_last_id(self) -> int:
        return max(map(lambda e: int(e.attrib['id']), self.tree.getroot()))

    # TODO check Publish

    async def add_event(self, form: cgi.FieldStorage, embed: Embed):
        """ Add an event to the calendar. """

        print('Debug: Chargement du webhook...')
        with open('/usr/local/src/URbot/wh', 'rb') as f:  # TODO clean up
            d = load(f)
            print('Debug: Webhook chargé !')

        wh_url, guild_id, channel_id = d[int(form.getvalue('user_id'))]

        async with ClientSession():
            webhook: Webhook = Webhook.from_url(wh_url)  # , adapter=AsyncWebhookAdapter(client))

            msg = await webhook.send("", wait=True, embed=embed, allowed_mentions=AllowedMentions(users=True))

        try:
            root = self.tree.getroot()
            root.set('last_id', str(int(root.get('last_id')) + 1))
            parent = et.SubElement(self.tree.getroot(), GAME_TAG, id=root.get('last_id'))

            for tag in TAGS:
                new_elmnt = et.SubElement(parent, tag)
                if tag in TAGS_TO_FORM:
                    new_elmnt.text = form.getvalue(TAGS_TO_FORM[tag], 'NotFound')
                elif tag == LINK_TAG:
                    new_elmnt.text = f"https://discord.com/channels/{guild_id}/{channel_id}/{msg.id}"
                elif tag == DATE_TAG:

                    date_string = form.getvalue(TAGS_TO_FORM[
                                                    DATE_TAG])  # On récupère la date en string (actuellement sous la forme 10/08/2021 11:00)
                    date = datetime.strptime(date_string,
                                             "%d/%m/%Y %H:%M")  # On transforme ce string en objet (Doit avoir la même mise en forme / / / : que le string cité ci-dessus)
                    date = date.strftime(
                        "%Y-%m-%d")  # On récupère uniquement la date sous la forme 2021-08-10, pour la compatibilité dans le calendrier web
                    # Ces changements de format ne concernent pas le message Discord, déjà posté, mais l'écriture dans le xml. Le calendrier php a besoin d'une date et heure sous ce format pour fonctionner

                    new_elmnt.text = date
                elif tag == TIME_TAG:

                    date_string = form.getvalue(TAGS_TO_FORM[
                                                    DATE_TAG])  # On récupère la date en string (actuellement sous la forme 10/08/2021 11:00)
                    date2 = datetime.strptime(date_string,
                                              "%d/%m/%Y %H:%M")  # On transforme ce string en objet (Doit avoir la même mise en forme / / / : que le string cité ci-dessus)
                    heure = date2.strftime("%Hh%M")  # On récupère uniquement l'heure, sous la forme 12h00
                    new_elmnt.text = heure
                else:
                    new_elmnt.text = TAGS_TO_LAMBDA[tag](form)
        except Exception as e:
            print(
                f"Problème lors de l'écriture dans le XML. Erreur : {e}")
            # Si l'écriture dans le xml ne marche pas, il ne faut pas que cela empêche de poster le message sur Discord

    def remove_event(self, ref, show_errors=True):  # TODO better name for show_errors
        root = self.tree.getroot()

        try:
            root.remove(next(e for e in root if e.get('id') == str(ref)))
        except StopIteration:
            if show_errors:
                error_log(f"Attempt to remove an event that doesn't exist. Event id : {ref}")
        else:
            log(f"Event with id {ref} successfully removed.")

    def remove_events(self, ids: str):
        """

        :param ids:
        """

        groups = ids.split(" ")

        for group in groups:
            if group.isnumeric():
                self.remove_event(group)
            elif re.match("^[0-9]*-[0-9]*$", group):
                start, end = (int(single_id) for single_id in group.split('-'))
                assert start <= end
                for single_id in range(start, end):
                    self.remove_event(single_id, show_errors=False)
            else:
                raise ValueError("Incorrect format of the ids' string.")

    def save(self):
        self.tree.write(self.fp, pretty_print=True)
