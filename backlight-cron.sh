#! /bin/bash

#numberPythonPrograms=$(ps aux | grep -c python)
#if [ "$numberPythonPrograms" != "1" ]
#then
#    echo "Running"
#else
#    echo "Stopped"
echo -e $"\xFE\x46" > /dev/ttyACM0
#fi
