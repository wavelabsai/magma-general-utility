#!/bin/bash
CPU_MEM_UTL_LOG_FILE=/var/core/cpu-mem-log.txt
if [ ! -f "$CPU_MEM_UTL_LOG_FILE" ]
then
    sudo touch $CPU_MEM_UTL_LOG_FILE 
fi

PID_MAGMAD=$(ps -eaf | grep python3 | grep magmad | awk '{print $2}')
PID_SUBSCRIBERDB=$(ps -eaf | grep python3 | grep subscriberdb | awk '{print $2}')
PID_DIRECTORYD=$(ps -eaf | grep python3 | grep directoryd | awk '{print $2}')
PID_ENODEBD=$(ps -eaf | grep python3 | grep enodebd | awk '{print $2}')
PID_POLICYDB=$(ps -eaf | grep python3 | grep policydb | awk '{print $2}')
PID_STATE=$(ps -eaf | grep python3 | grep state | awk '{print $2}')
PID_CTRACED=$(ps -eaf | grep python3 | grep ctraced | awk '{print $2}')
PID_SMSD=$(ps -eaf | grep python3 | grep smsd | awk '{print $2}')
PID_EVENTD=$(ps -eaf | grep python3 | grep eventd | awk '{print $2}')
PID_MOBILITYD=$(ps -eaf | grep python3 | grep mobilityd | awk '{print $2}')
PID_PIPELINED=$(ps -eaf | grep python3 | grep pipelined | awk '{print $2}')

PID_MME=$(pidof mme)
PID_SESSIOND=$(pidof sessiond)

date >> $CPU_MEM_UTL_LOG_FILE
echo "_________________________________________________" >> $CPU_MEM_UTL_LOG_FILE
echo "MAGMA :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_MAGMAD -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE 
echo "SUBSCRIBERDB :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_SUBSCRIBERDB -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "DIRECTORYD :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_DIRECTORYD  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "ENODEBD :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_ENODEBD  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "POLICYDB :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_POLICYDB  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "STATE :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_STATE  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "CTRACED :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_CTRACED  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "SMSD :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_SMSD  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "EVEND : " >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_EVENTD  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "MOBILITYD :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_MOBILITYD  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "PIPELINED :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_PIPELINED  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "MME :" >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_MME  -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
echo "SESSIOND : " >> $CPU_MEM_UTL_LOG_FILE
  ps -p $PID_SESSIOND -o %cpu,%mem >> $CPU_MEM_UTL_LOG_FILE
