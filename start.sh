#!/bin/bash
# This script starts the discord bot of "L'Union des Rôlistes"

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com

# start / restart the service
echo "Starting..."
sudo systemctl restart Bot_Base

# wait a little to find out if the bot was successfully started
sleep 1

# check SubState
sub_state=$(systemctl show -p SubState Bot_Base --value)

if [ "$sub_state" = "running" ]; then
  echo "Success!"
else
  echo "Failure... (use 'journalctl -eu Bot_Base' to check the log.)"
fi