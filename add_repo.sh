#!/bin/bash
# This script starts the discord bot of "L'Union des Rôlistes"

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com

# TODO : Add commands verifications with $? (renvoie souvent 0 si tout se passe bien)
tmp='/usr/local/src'          #'tmp/ur_bot/cogs'
ur_bot_dir='/usr/local/src/URbot'
cogs_folder="$ur_bot_dir/bot/cogs"
repo="$tmp/$1"
src="$repo/src"
a2=/etc/apache2
www=/var/www/html

# checks repo name has been supplied
if [ -z ${1+x} ]; then
  echo 'error: argument not supplied'
  echo
  echo 'usage : ./add_repo.sh <repo_name>'
  exit
fi

if [ ! -d "$repo" ] ; then
  # downloads the repo from github.com
  git clone "https://github.com/UnionRolistes/$1.git" "$repo" # TODO add several cogs at once

  # checks that the clone was successful
  if [ $? != 0 ]; then
    echo Failure
    exit
  fi
else
  # updates the repo
  cd "$repo" || exit
  #git checkout . --> Dit qu'on est sur aucune branche. Problème, les branches n'ont pas toute une branche master (parfois main), donc on ne peut pas rajouter git pull origin master pour l'instant
  git stash
  git pull
fi

# installs cogs (located in the src folder and starting with 'cog_')
echo ------------ TEXT: Installing cogs... ------------
if [ ! -d $cogs_folder ] ; then
  mkdir $cogs_folder
fi
find "$src" -maxdepth 1 -name "cog_*" -exec cp -vra '{}' $cogs_folder \;
echo

# installs locale
if [ -d "$src/locale" ]; then
  echo ------------ TEXT: Installing translations... ------------
  echo
  cp -vra "$src/locale/." "$ur_bot_dir/locale"
fi

echo ------------ TEXT: Installation complete. ------------

# installs www
if [ -d "$src/www" ]; then
  if [ ! -d "$www/$1" ]; then
    mkdir -v "$www/$1"
  fi
  cp -vra "$src/www/." "$www/$1"
  chmod -R 775 "$www/$1"
fi

# installs virtualhosts
#if [ -d "$src/sites-available" ]; then
#  echo ------------ TEXT: Installing virtualhosts... ------------
#  cp -vra "$src/sites-available/." "$a2/sites-available"
#  for f in "$src/sites-available/*.conf"; do
#    ln -s $a2/sites-available/$f $a2/sites-enabled/$f
#    a2ensite "$(basename "$f")"
#  done
#  systemctl reload apache2
#fi

# TODO bash 3 +
# TODO add installation of the cog's requirements.txt
