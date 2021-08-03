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
install_folder="/usr/local/src/URbot"
src="src"
bot_pckg_name='bot'
bot_pckg="$src/$bot_pckg_name"
urpy_pckg="$src/urpy"
# TODO better variables

python='python3.7'
venv='/opt/virtualenv/URBot'
bin="$venv/bin/"
service='Bot_Base.service'
requirements="$urpy_pckg/requirements.txt"

# Installs required softwares
sudo apt update
sudo apt install -y $python
sudo apt install -y $python-venv
sudo apt install -y python3-venv
sudo apt install -y $python-dev
sudo apt install -y build-essential

# Creates a python virtualenv
sudo $python -m venv $venv
source $bin/activate
sudo $bin/pip install -r "$requirements"
deactivate

# Copies python code to install folder
sudo mkdir $install_folder
sudo cp -vra "$src/bot" $install_folder
sudo cp -vra "$src/start.py" $install_folder
sudo cp -vra "$src/locale" $install_folder
sudo cp -vra "$src/urpy" $venv/lib/$python/site-packages
# rush
sudo chmod -R 755 $install_folder
sudo chown "$USER" $install_folder


# Copies .service to /etc/systemd/system
sudo cp -v src/$service /etc/systemd/system
sudo systemctl enable $service

echo

# Reads and writes token into root folder
if [ ! -e $install_folder/.bot_token ]; then
  echo '|~ Veuillez entrer le token du bot :'
  read -r bot_token
  echo "$bot_token" | sudo tee $install_folder/.bot_token > /dev/null
  echo
  exit
fi
if [ -e $install_folder/.bot_token ]; then
  echo '\e[1;31m ## Token déjà saisi \e[0m'
  echo
  exit
fi

echo '\e[1;31m ## Installation du bot terminée\e[0m'
echo

echo '\e[1;31m ## Begin webserver installation \e[0m'
echo

apt install -y apache2
apt install -y php
apt install -y libapache2-mod-php  # TODO check if necessary
apt install -y php-xml
apt install -y php-curl
a2enmod cgid
systemctl restart apache2

# TODO add user name
