# URbot (Bot_Base + Bot_Planning_python + Bot_Presentation) — dockerized
#
# Reproduit la structure trouvée sur le VPS dans /usr/local/src/URbot :
#   bot/urbot.py          <- coeur du bot (repo Bot_Base ; fichier réel en
#                            minuscules malgré la casse "URbot" mentionnée
#                            dans l'investigation initiale, cf. start.py)
#   bot/cogs/cog_planning     <- copié depuis Bot_Planning_python/src/cog_planning (add_repo.sh)
#   bot/cogs/cog_presentation <- copié depuis Bot_Presentation/src/cog_presentation (add_repo.sh)
#   urpy/                 <- lib interne installée dans site-packages (requirements.txt ici)
#   start.py              <- point d'entrée : "from bot.urbot import main"
#
# Version Python : 3.7, identique à celle codée en dur dans Bot_Base/install.sh
# ($python='python3.7'), qui est la version utilisée pour créer le venv du bot
# sur le VPS (/opt/virtualenv/URBot), même si le système hôte a depuis été mis
# à niveau vers Python 3.13.5.
FROM python:3.7-slim

# Dépendances système équivalentes à celles installées par install.sh
# (python3.7-dev / build-essential) pour compiler les paquets natifs (lxml).
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/src

# --- Récupération des 3 repos ---
# Clone direct depuis GitHub (même source que add_repo.sh sur le VPS :
# https://github.com/UnionRolistes/<repo>.git), pour rester fidèle au
# processus d'assemblage réel plutôt que de dépendre d'un contexte de build
# local qui devrait déjà contenir les 3 repos en sous-dossiers.
ARG GIT_ORG=https://github.com/UnionRolistes
RUN git clone --depth 1 ${GIT_ORG}/Bot_Base.git Bot_Base \
 && git clone --depth 1 ${GIT_ORG}/Bot_Planning_python.git Bot_Planning_python \
 && git clone --depth 1 ${GIT_ORG}/Bot_Presentation.git Bot_Presentation

# --- Assemblage façon add_repo.sh : URbot = Bot_Base + cogs copiés dedans ---
RUN mkdir -p URbot \
 && cp -r Bot_Base/src/. URbot/ \
 && mkdir -p URbot/bot/cogs \
 && cp -r Bot_Planning_python/src/cog_planning URbot/bot/cogs/cog_planning \
 && cp -r Bot_Presentation/src/cog_presentation URbot/bot/cogs/cog_presentation

# bot/urbot.py fait `from Bot_Base.src.urpy import ...` (import package absolu)
# et `from cog_about import About` / `import settings` (imports bruts résolus
# via bot/ lui-même). Le clone Bot_Base original est donc conservé sur le
# disque (jamais supprimé) et /usr/local/src + /usr/local/src/URbot/bot sont
# ajoutés à PYTHONPATH pour reproduire l'environnement d'exécution du VPS.
ENV PYTHONPATH="/usr/local/src:/usr/local/src/URbot/bot"

WORKDIR /usr/local/src/URbot

# --- Dépendances Python : combinaison des 3 requirements.txt trouvés ---
# - urpy/requirements.txt (Bot_Base)      : discord, requests, lxml
# - cog_planning/requirements.txt          : vide (aucune dépendance déclarée)
# - cog_presentation/requirements.txt      : vide (aucune dépendance déclarée)
RUN cat urpy/requirements.txt \
    bot/cogs/cog_planning/requirements.txt \
    bot/cogs/cog_presentation/requirements.txt \
    2>/dev/null | sed '/^\s*$/d' | sort -u > /tmp/requirements.txt \
 && cat /tmp/requirements.txt \
 && pip install --no-cache-dir -r /tmp/requirements.txt

# urpy est une lib interne copiée dans site-packages sur le VPS
# (venv/lib/$python/site-packages) ; on reproduit ça ici.
RUN cp -r urpy "$(python3 -c 'import site; print(site.getsitepackages()[0])')/urpy"

# Fichiers de stockage webhook créés par install.sh, avec permissions larges
# (chmod 776 sur le VPS).
RUN touch wh whPrez && chmod 776 wh whPrez

# NOTE: .bot_token n'est JAMAIS copié dans l'image. Il est fourni au runtime
# via un volume monté par docker-compose (cf. docker-compose.yml).

# Point d'entrée identique à /usr/local/src/URbot/start.py sur le VPS :
#   #!/opt/virtualenv/URBot/bin/python
#   from bot.urbot import main
#   if __name__ == '__main__':
#       main()
COPY start.py /usr/local/src/URbot/start.py

CMD ["python3", "start.py"]
