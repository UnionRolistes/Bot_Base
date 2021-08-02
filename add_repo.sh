#!/bin/bash
# This script starts the discord bot of "L'Union des Rôlistes"
# TODO add copyright to follow bash scripts rules
tmp='/tmp/ur_bot/cogs'
ur_bot_dir='/usr/local/bin/URbot'
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

if [ ! -e "$repo" ] ; then
  # downloads the repo from github.com
  git clone "https://github.com/UnionRolistes/$1.git" "$repo" # TODO add several cogs at once

  # checks that the clone was successful
  if [ ! -e "$repo" ]; then
    echo Failure
    exit
  fi
else
  # updates the repo
  cd "$repo" || exit
  git pull
fi

# installs cogs (located in the src folder and starting with 'cog_')
echo Installing cogs...
if [ ! -e $cogs_folder ] ; then
  mkdir $cogs_folder
fi
find "$src" -maxdepth 1 -name "cog_*" -exec cp -vra '{}' $cogs_folder \;
echo

# installs locale
echo Installing translations...
cp -vra "$src/locale/." "$ur_bot_dir/locale"
echo

echo Installation complete.

# installs www
if [ -e "$src/www" ]; then
  if [ ! -e "$www/$1" ]; then
    mkdir -v "$www/$1"
  fi
  cp -vra "$src/www/." "$www/$1"
fi

# installs virtualhosts
#if [ -e "$src"/sites-available ]; then
 # cp -vra "$src"/sites-available/. $a2/sites-available
 # for f in "$src"/sites-available/*.conf; do
#    a2ensite "$(basename "$f")"
 # done
 # systemctl reload apache2
# fi

# TODO bash 3 +
# TODO add installation of locale folder
# TODO add installation of the cog's requirements.txt
