#!/bin/bash
# This script updates the files for the discord bot of "L'Union des Rôlistes", and restart it

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com

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