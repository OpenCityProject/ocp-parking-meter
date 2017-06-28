#! /bin/bash

scriptRunning=$(ps aux | grep -c script.py)
if [ "$scriptRunning" != "1" ] # 1 means only ps aux command, expecting 2 (ps aux plus python script.py)
then
   echo "Already running"
else
   echo "Script stopped. Rebooting"
   nohup python script.py >/dev/null 2>&1 &
fi

