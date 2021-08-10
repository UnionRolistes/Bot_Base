#!/bin/bash
# This script starts the discord bot of "L'Union des Rôlistes"
# TODO add copyright to follow bash scripts rules
tmp='/usr/local/src'            #'tmp/ur_bot/cogs'
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
  if [ ! -d "$repo" ]; then
    echo Failure
    exit
  fi
else
  # updates the repo
  cd "$repo" || exit
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
fi

# installs virtualhosts
if [ -d "$src/sites-available" ]; then
  echo ------------ TEXT: Installing virtualhosts... ------------
  cp -vra "$src/sites-available/." "$a2/sites-available"
  for f in "$src/sites-available/*.conf"; do
    a2ensite "$(basename "$f")"
  done
  systemctl reload apache2
fi

# TODO bash 3 +
# TODO add installation of the cog's requirements.txt
