#!/bin/bash
# Delete the files in /var/core which are old then 1 day
echo "Clean up cronjob"
find /var/core/ -type f -mtime +1 -exec sudo rm -rf  {} +

# Delete the gz files in /var/log directory
find /var/log/*gz -type f -mtime +1 -exec sudo rm -rf  {} +
