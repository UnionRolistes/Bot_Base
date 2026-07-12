import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

import httpx
from fastapi import FastAPI, HTTPException
from lxml import etree as et
from pydantic import BaseModel

app = FastAPI()

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
EVENTS_XML_PATH = DATA_DIR / "events.xml"
WEBHOOKS_JSON_PATH = DATA_DIR / "webhooks.json"

# Union des Rolistes © 2020 by "Association Union des Rôlistes & co" is licensed under
# Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)

# Repris tel quel de Web_Planning/src/www/cgi/modele_fiche_planning.txt (partie avant le
# "[" : la partie après contient des notes de réactions jamais utilisées par le CGI d'origine).
ANNOUNCEMENT_TEMPLATE = """
 **Type ** {type}
:calendar: ** Date ** Le {date}
:earth_americas: ** Fuseau horaire ** {horaire}
:clapper: **Titre** {title}
:timer:  ** Durée moyenne du scénario ** {length}
:person_standing_tone1: ** Nombre de joueurs ** {players}
:crown: **MJ** {pseudoMJ}
:d10: ** Système** {system}
:baby::skin-tone-1: **PJ Mineur ** {minors_allowed}
:star2: ** Plateformes ** {platforms}
:grey_question: ** Détails**
{details}

** Participe ** ✅ / ** Ne participe pas ❌ **
"""

# Ordre et valeurs alignés sur Web_Planning/src/www/cgi/const.py (MinorsAllowed), qui est
# ce que le formulaire réel envoie (jdr_pj radio : 0/1/2) - à ne pas confondre avec l'enum à
# 4 valeurs de cog_planning/const.py, utilisée ailleurs par le bot pour un usage différent.
MINORS_ALLOWED = {0: "oui", 1: "non préférable", 2: "non"}

# Ordre des balises XML repris de Bot_Base/src/urpy/xml.py (Calendar.TAGS), pour rester
# compatible avec le format lu par le rendu PHP du calendrier.
XML_TAGS_ORDER = [
    "titre", "capacite", "minimum", "inscrits", "date", "heure", "duree",
    "type", "mj", "systeme", "pjMineur", "plateformes", "details", "lien",
]

_webhooks: dict = {}


def _load_webhooks() -> None:
    if WEBHOOKS_JSON_PATH.exists():
        _webhooks.update({int(k): v for k, v in json.loads(WEBHOOKS_JSON_PATH.read_text()).items()})


def _save_webhooks() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WEBHOOKS_JSON_PATH.write_text(json.dumps(_webhooks))


_load_webhooks()


class WebhookRegistration(BaseModel):
    user_id: int
    webhook_url: str
    guild_id: int
    channel_id: int


class EventCreate(BaseModel):
    user_id: int
    pseudo: str
    jdr_type: str
    jdr_title: str
    jdr_date: str  # format "dd/mm/YYYY HH:MM", produit par le sélecteur tail.DateTime du formulaire
    jdr_horaire: str  # fuseau horaire choisi (ex. "GMT +1"), pas une heure
    jdr_length: str
    jdr_system: str
    jdr_pj: int  # 0/1/2, voir MINORS_ALLOWED
    platform: List[str] = []
    jdr_details: str
    min_joueurs: int
    max_joueurs: int


def _load_calendar() -> et._ElementTree:
    if not EVENTS_XML_PATH.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        et.ElementTree(et.Element("parties", last_id="0")).write(str(EVENTS_XML_PATH), pretty_print=True)
    return et.parse(str(EVENTS_XML_PATH), et.XMLParser(remove_blank_text=True))


@app.post("/webhooks")
def register_webhook(reg: WebhookRegistration):
    """Enregistre le webhook du salon d'annonce pour un utilisateur (appelé par $jdr)."""
    _webhooks[reg.user_id] = reg.dict()
    _save_webhooks()
    return {"ok": True}


@app.post("/events")
async def create_event(event: EventCreate):
    """Envoie l'annonce Discord via webhook et persiste l'événement dans events.xml."""
    webhook = _webhooks.get(event.user_id)
    if webhook is None:
        raise HTTPException(
            status_code=404,
            detail="Aucun webhook enregistré pour cet utilisateur, relancez $jdr sur Discord.",
        )

    try:
        dt = datetime.strptime(event.jdr_date, "%d/%m/%Y %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide, attendu dd/mm/YYYY HH:MM.")

    players = (
        str(event.max_joueurs)
        if event.max_joueurs == event.min_joueurs
        else f"{event.max_joueurs} (min {event.min_joueurs})"
    )
    minors_allowed = MINORS_ALLOWED.get(event.jdr_pj, "?")
    mj = f"<@{event.user_id}> [{event.pseudo}]"
    platforms = " ".join(event.platform)

    description = ANNOUNCEMENT_TEMPLATE.format(
        type=event.jdr_type,
        date=event.jdr_date,
        horaire=event.jdr_horaire,
        title=event.jdr_title,
        length=event.jdr_length,
        players=players,
        pseudoMJ=mj,
        system=event.jdr_system,
        minors_allowed=minors_allowed,
        platforms=platforms,
        details=event.jdr_details,
    )

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{webhook['webhook_url']}?wait=true",
            json={"embeds": [{"type": "rich", "description": description}]},
        )
        if resp.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"Échec de l'envoi Discord : {resp.status_code} {resp.text}")
        message = resp.json()

    tree = _load_calendar()
    root = tree.getroot()
    new_id = int(root.get("last_id", "0")) + 1
    root.set("last_id", str(new_id))

    lien = f"https://discord.com/channels/{webhook['guild_id']}/{webhook['channel_id']}/{message['id']}"
    values = {
        "titre": event.jdr_title,
        "capacite": str(event.max_joueurs),
        "minimum": str(event.min_joueurs),
        "inscrits": "0",
        "date": dt.strftime("%Y-%m-%d"),
        "heure": dt.strftime("%Hh%M"),
        "duree": event.jdr_length,
        "type": event.jdr_type,
        "mj": mj,
        "systeme": event.jdr_system,
        "pjMineur": minors_allowed,
        "plateformes": platforms,
        "details": event.jdr_details,
        "lien": lien,
    }

    partie = et.SubElement(root, "partie", id=str(new_id))
    for tag in XML_TAGS_ORDER:
        et.SubElement(partie, tag).text = values[tag]
    tree.write(str(EVENTS_XML_PATH), pretty_print=True)

    return {"id": new_id, "lien": lien}


@app.get("/health")
def health():
    return {"ok": True}
