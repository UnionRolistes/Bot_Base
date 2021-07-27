#!/bin/bash
# This script starts the discord bot of "L'Union des Rôlistes"
# TODO add copyright to follow bash scripts rules

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