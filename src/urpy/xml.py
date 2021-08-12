import pickle
from pathlib import Path

import discord
from discord import Webhook, AsyncWebhookAdapter
from aiohttp import ClientSession
from lxml import etree as et
import cgi
from urpy.utils import error_log, log
from urpy.localization import lcl, Localization
import re
from datetime import datetime

game_tag = 'partie'
title_tag = 'titre'
max_players_tag = 'capacite'
min_players_tag = 'minimum'
nb_joined_tag = 'inscrits'
date_tag = 'date'
time_tag = 'heure'
length_tag = 'duree'
type_tag = 'type'
mj_tag = 'mj'
system_tag = 'systeme'
minors_allowed_tag = 'pjMineur'
platforms_tag = 'plateformes'
details_tag = 'details'
link_tag = 'lien'

tags = [title_tag, max_players_tag, min_players_tag, nb_joined_tag,
        date_tag, time_tag, length_tag, type_tag, mj_tag, system_tag,
        minors_allowed_tag, platforms_tag, details_tag, link_tag]

tags_to_form = {
    title_tag: 'jdr_title',
    max_players_tag: 'maxJoueurs',
    min_players_tag: 'minJoueurs',
    date_tag: 'jdr_date',
    length_tag: 'jdr_length',
    type_tag: 'jdr_type',
    system_tag: 'jdr_system',
    minors_allowed_tag: 'jdr_pj',
    details_tag: 'jdr_details',
}

tags_to_lambda = {
    nb_joined_tag: lambda f: '0',
    time_tag: lambda f: '15h00',
    mj_tag: lambda f: f"<@{f.getvalue('user_id')}> [{f.getvalue('pseudo')}]",
    platforms_tag: lambda f: " ".join(f.getlist('platform')),
    link_tag: lambda f: 'https://discord.com/channels/TODO'
}

_ = lcl


class Calendar:
    """
    This class allows updating an xml file that contains the data of an event calendar.
    """
    creators_to_webhook = {}

    def __init__(self, fp: str, localization: Localization = None):  # TODO localization
        """
        Create an xmlCalendar.

        @fp path to xml file
        """
        self.fp = fp
        import os
        from urpy import utils
        #utils.html_header_content_type()
        #print(os.listdir("/usr/share/urbot/"))
        #print(open("/usr/share"))
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

    async def add_event(self, form: cgi.FieldStorage, embed: discord.Embed):
        """ Add an event to the calendar. """

        print('Debug: Chargement du webhook...')
        with open(f'/usr/local/src/URbot/wh', 'rb') as f:  # TODO clean up
            d = pickle.load(f)
            print('Debug: Webhook chargé !')
            
        wh_url, guild_id, channel_id = d[int(form.getvalue('user_id'))]

        async with ClientSession() as client:
            webhook: Webhook = Webhook.from_url(wh_url, adapter=AsyncWebhookAdapter(client))

            msg = await webhook.send("", wait=True, embed=embed, allowed_mentions=discord.AllowedMentions(users=True))
        root = self.tree.getroot()
        root.set('last_id', str(int(root.get('last_id')) + 1))
        parent = et.SubElement(self.tree.getroot(), game_tag, id=root.get('last_id'))

        for tag in tags:
            new_elmnt = et.SubElement(parent, tag)
            if tag in tags_to_form:
                new_elmnt.text = form.getvalue(tags_to_form[tag], 'NotFound')
            elif tag == link_tag:
                new_elmnt.text = f"https://discord.com/channels/{guild_id}/{channel_id}/{msg.id}"
            elif tag == time_tag:

                date_string = form.getvalue(tags_to_form[date_tag]) #On récupére la date en string (actuellement sous la forme 10/08/2021 11:00)
                date = datetime.strptime(date_string, "%d/%m/%Y %H:%M") #On transforme ce string en objet (Doit avoir la même mise en forme / / / : que le string cité ci-dessus)
                heure = date.strftime("%Hh%M") #On récupère uniquement l'heure, sous la forme 12h00
                new_elmnt.text = heure

            elif tag == date_tag:

                date_string = form.getvalue(tags_to_form[date_tag]) #On récupére la date en string (actuellement sous la forme 10/08/2021 11:00)
                date = datetime.strptime(date_string, "%d/%m/%Y %H:%M") #On transforme ce string en objet (Doit avoir la même mise en forme / / / : que le string cité ci-dessus)
                date = date.strftime("%Y-%m-%d")#On récupère uniquement la date sous la forme 2021-08-10, pour la compatibilité dans le calendrier web
                #Ces changements de format ne concernent pas le message Discord, déjà posté, mais l'écriture dans le xml. Le calendrier php a besoin d'une date et heure sous ce format pour fonctionner

                new_elmnt.text = date
            else:
                new_elmnt.text = tags_to_lambda[tag](form)

    def remove_event(self, id, show_errors=True):  # TODO better name for show_errors
        root = self.tree.getroot()

        try:
            root.remove(next(e for e in root if e.get('id') == str(id)))
        except StopIteration:
            if show_errors:
                error_log(f"Attempt to remove an event that doesn't exist. Event id : {id}")
        else:
            log(f"Event with id {id} successfully removed.")

    def remove_events(self, ids: str):
        """

        :param ids:
        """

        groups = ids.split(" ")

        for group in groups:
            if group.isnumeric():
                self.remove_event(group)
            elif re.match("^[0-9]*-[0-9]*$", group):
                start, end = (int(id) for id in group.split('-'))
                assert start <= end
                for id in range(start, end):
                    self.remove_event(id, show_errors=False)
            else:
                raise ValueError("Incorrect format of the ids' string.")

    def save(self):
        self.tree.write(self.fp, pretty_print=True)
