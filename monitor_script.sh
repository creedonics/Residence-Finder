#!/bin/bash

# Path to the Python script
SCRIPT="/Path/to/your/script/ResCheckAll.py" 

# Path to the Log file
LOGFILE="/Path/to/your/script/logfile.log" 

# Function to start the script
start_script() {
    echo "$(date): Starting script" >> "$LOGFILE"
    python3 "$SCRIPT" >> "$LOGFILE" 2>&1 &
    echo $! > /tmp/ResCheckAll.pid
}

# Function to stop the script
stop_script() {
    if [ -f /tmp/ResCheckAll.pid ]; then
        kill $(cat /tmp/ResCheckAll.pid)
        rm /tmp/ResCheckAll.pid
    fi
}

# Trap SIGINT to stop the script
trap 'echo "$(date): Stopping script" >> "$LOGFILE"; stop_script; exit 0' SIGINT

# Monitor loop
while true; do
    if [ -f /tmp/ResCheckAll.pid ]; then
        if ! ps -p $(cat /tmp/ResCheckAll.pid) > /dev/null 2>&1; then
            echo "$(date): Script not running, restarting" >> "$LOGFILE"
            start_script
        fi
    else
        echo "$(date): PID file not found, starting script" >> "$LOGFILE"
        start_script
    fi
    sleep 10
done
