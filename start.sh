# start / restart the service
sudo systemctl restart Bot_Base

# wait a little to find out if the service was successfully started
sleep 1

# check SubState
sub_state=$(systemctl show -p SubState Bot_Base --value)

if [ "$sub_state" = "running" ]; then
  echo "Success!"
else
  echo "Failure... Use 'journalctl -eu Bot_Base -e' to check the logs."
fi