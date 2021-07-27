# start / restart the service
sudo systemctl restart Bot_Base

# wait a little to find out if the service was successfully started
sleep 1

# check SubState
sub_state=$(systemctl show -p SubState Bot_Base --value)

if [ "$sub_state" = "running" ]; then
  echo "Bot successfully started !"
else
  echo "Failure... Use 'systemctl status Bot_Base' for more information."
fi