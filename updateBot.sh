#!/bin/bash
# This script updates the files for the discord bot of "L'Union des Rôlistes"
# TODO add copyright to follow bash scripts rules

cd /usr/local/src/Bot_Base
git pull #Pour mettre à jour le script add_repo.sh
bash add_repo.sh Bot_Base
bash install.sh
bash add_repo.sh Bot_Planning_python
bash add_repo.sh Web_Planning
bash add_repo.sh Web_Presentation
bash add_repo.sh Bot_Presentation

service apache2 restart
bash start.sh