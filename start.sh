sudo systemctl restart Bot_Base

sub_state=$(systemctl show -p SubState Bot_Base --value)

if [ "$sub_state" = "running" ]; then
  echo "Bot successfully started !"
else
  echo "Failure... Use 'systemctl status Bot_Base' for more information."
fi