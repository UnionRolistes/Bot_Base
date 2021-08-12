# Bot_Base
sudo git clone https://github.com/UnionRolistes/Bot_Base.git && cd Bot_Base


# Installation
Pour une 1ère installation : 
"cd /usr/local/src && sudo git clone https://github.com/UnionRolistes/Bot_Base && cd Bot_Base && sudo bash updateBot.sh"

Pour une mise à jour :
"cd /usr/local/src/Bot_Base && sudo git checkout . && sudo git pull && sudo bash updateBot.sh"



How to setup URbot - The discord bot for managing servers dedicated to
rpgs

1) Install a linux based OS (we'll be using Debian as a reference)
2) Install git
3) "cd /usr/local/src && sudo git clone https://github.com/UnionRolistes/Bot_Base && cd Bot_Base && sudo bash updateBot.sh". It installs the bot and the 2 sub features : 1. Bot_Planning and Web_Planning 2. Bot_Presentation and Web_Presentation

4) If you want to choose the features to install --> "cd /usr/local/src/Bot_Base && sudo git pull && sudo bash install.sh"
Then "sudo bash <name of repo on github>"

5) Start the bot and the web sites with "cd/usr/local/src/Bot_Base && sudo bash start.sh && sudo service apache2 restart "


How to collaborate

1) Make sure auto crlf is on


**credit / contributeur**
Voir src/bot/info/credits.txt

**donation link**
http://site.unionrolistes.fr/
