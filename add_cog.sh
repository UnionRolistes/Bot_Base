#!/bin/bash
# This script starts the discord bot of "L'Union des Rôlistes"
# TODO add copyright to follow bash scripts rules
tmp='/tmp/ur_bot/cogs'
cogs_folder='/usr/local/bin/URbot/bot/cogs'
repo="$tmp/$1"

# checks repo name has been supplied
if [ -z ${1+x} ]; then
  echo 'error: argument not supplied'
  echo
  echo 'usage : ./add_cog.sh <repo_name>'
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

cp -vr "$repo/src/." $cogs_folder
