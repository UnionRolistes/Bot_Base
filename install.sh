#!/bin/bash
# This script installs the discord bot of "L'Union des Rôlistes"
#
# Copyright 2021 Florian Delprat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Variables
python='python3.9'
venv='/opt/virtualenv/URBot'
bin="$venv/bin/"
pckg_name='bot'
python_package="src/$pckg_name"
service='src/URbot.service'
requirements="$python_package/requirements.txt"

# Installs required softwares
sudo apt update
sudo apt-get install $python
sudo apt-get install $python-venv

# Creates a python virtualenv
sudo $python -m venv $venv
source $bin/activate
sudo $bin/pip install -r $requirements
deactivate

# Copies python code to usr/local/sbin
sudo cp -vr $python_package /usr/local/bin
# rush
sudo cp -vr 'src/urpy' $venv/lib/$python/site-packages
sudo chmod -R 755 /usr/local/bin/$pckg_name
sudo chown "$USER" /usr/local/bin/$pckg_name


# Copies .service to /etc/systemd/system
sudo cp -v $service /etc/systemd/system
sudo systemctl enable URbot.service

# Reads and writes token into root folder
echo
echo '|~ Veuillez entrer le token du bot :'
read -r bot_token
echo "$bot_token" | sudo tee /root/.bot_token > /dev/null
exit

echo
echo 'Installation terminée.'
echo




