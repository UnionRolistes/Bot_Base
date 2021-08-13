#!/bin/bash
# This script installs the discord bot of "L'Union des Rôlistes"

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com

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
  echo '------------ TEXT: |~ Veuillez entrer le token du bot : ------------'
  read -r bot_token
  echo "$bot_token" | sudo tee $install_folder/.bot_token > /dev/null
  echo
  exit
fi
if [ -e $install_folder/.bot_token ]; then
  echo '------------ TEXT: Token déjà saisi ------------'
  echo
  exit
fi

echo '------------ TEXT: Creation des fichiers de stockage webhook ------------'
echo
# Create 2 files for webhook storing
if [ ! -e $install_folder/wh ]; then
  touch $install_folder/wh
  chmod 776 $install_folder/wh
  exit
fi
if [ ! -e $install_folder/whPrez ]; then
  touch $install_folder/whPrez
  chmod 776 $install_folder/wh
  exit
fi

echo '------------ TEXT: Installation du bot terminée ------------'
echo

echo '------------ TEXT: Begin webserver installation ------------'
echo

apt install -y apache2
apt install -y php
apt install -y libapache2-mod-php  # TODO check if necessary
apt install -y php-xml
apt install -y php-curl
a2enmod cgid
systemctl restart apache2

# TODO add user name
