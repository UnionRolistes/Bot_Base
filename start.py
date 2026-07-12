#!/usr/bin/env python3
# Equivalent de /usr/local/src/URbot/start.py sur le VPS.
# Sur le VPS le shebang pointe directement sur l'interpreteur du venv
# (#!/opt/virtualenv/URBot/bin/python) ; ici l'image ne contient qu'un seul
# interpreteur Python (celui de l'image de base), donc CMD l'invoque
# directement (cf. Dockerfile).
#
# NOTE : le module source réel dans le repo Bot_Base est bot/urbot.py
# (minuscules). L'investigation VPS notait "from bot.URbot import main" mais
# le clone git (filesystem Linux, sensible à la casse) ne contient que
# bot/urbot.py - la casse "URbot" vient probablement d'une lecture sur un
# systeme de fichiers insensible a la casse ou d'un rename historique. On
# importe donc bot.urbot ici, qui expose bien la fonction main() attendue.
from bot.urbot import main

if __name__ == '__main__':
    main()
