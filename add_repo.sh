#!/bin/bash
# This script starts the discord bot of "L'Union des Rôlistes"
# TODO add copyright to follow bash scripts rules
tmp='/tmp/ur_bot/cogs'
ur_bot_dir='/usr/local/bin/URbot'
cogs_folder="$ur_bot_dir/bot/cogs"
repo="$tmp/$1"

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
if [ ! -e "$cogs_folder" ] ; then
  mkdir $cogs_folder
fi
find "$repo/src/" -maxdepth 1 -name "cog_*" -exec cp -vr '{}' $cogs_folder \;
echo

# installs locale
echo Installing translations...
cp -vr "$repo/src/locale/." "$ur_bot_dir/locale"
echo

echo Installation complete.
# TODO bash 3 +
# TODO add installation of locale folder
# TODO add installation of the cog's requirements.txt
