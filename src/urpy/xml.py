import discord
from lxml import etree as et
import cgi
from urpy.utils import error_log, log
from urpy.localization import lcl, Localization
import re

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
link_tag = 'link'

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
    time_tag: lambda f: 'TODO time',
    mj_tag: lambda f: f"<@{f.getvalue('user_id')}> [{f.getvalue('pseudo')}]",
    platforms_tag: lambda f: " ".join(f.getlist('platform')),
    link_tag: lambda f: 'TODO link'
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
        webhook: discord.Webhook = Calendar.creators_to_webhook[form.getvalue('user_id')]
        msg = await webhook.send("", wait=True, embed=embed, allowed_mentions=discord.AllowedMentions(users=True))
        root = self.tree.getroot()
        root.set('last_id', str(int(root.get('last_id')) + 1))
        parent = et.SubElement(self.tree.getroot(), game_tag, id=root.get('last_id'))

        for tag in tags:
            new_elmnt = et.SubElement(parent, tag)
            if tag in tags_to_form:
                new_elmnt.text = form.getvalue(tags_to_form[tag], 'NotFound')
            elif tag == link_tag:
                new_elmnt.text = msg.jump_url
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
