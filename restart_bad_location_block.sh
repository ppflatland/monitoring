#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"


if ! pgrep -l -f -x "/usr/bin/python3 ${SCRIPTPATH}/core.py" > /dev/null
then
    #echo 'Warning! bad_location_block process don`t found.Restarting...'
    /usr/bin/python3 ${SCRIPTPATH}/core.py >/dev/null 2>&1 &
else
    TAIL_PID=$(ps aux | grep $(echo "/home/flatland/python/web_monitoring/core.py" | sed "s/^\(.\)/[\1]/g") | awk '{print $2}')
    #echo "PID $TAIL_PID"
    #echo "Found bad_location_block process.Restarting..."
    kill $TAIL_PID
    sleep 2
    pgrep phantomjs | xargs kill 
    /usr/bin/python3 ${SCRIPTPATH}/core.py >/dev/null 2>&1 &
    
fi
