#!/bin/bash
CPU_MEM_UTL_LOG_FILE=/var/core/cpu-mem-log.txt
if [ ! -f "$CPU_MEM_UTL_LOG_FILE" ]
then
    sudo touch $CPU_MEM_UTL_LOG_FILE
fi

print_python_cpu_mem_usage() {
  echo "PRINTING FOR $1"
  process_id=$1

  PID_NEW_PROCESS=$(ps -eaf | grep python3 | grep $1 | awk 'NR==1{print $2}')
  if [[ -z PID_NEW_PROCESS ]]; then   echo "$1 DOESNOT EXISTS"; fi

  CPU_MEM_DUMP=$(ps -p $PID_NEW_PROCESS -o %cpu,%mem | awk NR==2)
  echo $CPU_MEM_DUMP : $1" ("$PID_NEW_PROCESS")" >> $CPU_MEM_UTL_LOG_FILE
}

print_c_cpu_mem_usage() {

  PID_MME=$(pidof mme)
  PID_SESSIOND=$(pidof sessiond)

  if [[ -z PID_MME ]]; then   echo "MME DOESNOT EXISTS"; fi
  if [[ -z PID_SESSIOND ]]; then   echo "SESSIOND DOESNOT EXISTS"; fi

  CPU_MEM_DUMP_MME=$(ps -p $PID_MME -o %cpu,%mem | awk NR==2)
  echo $CPU_MEM_DUMP_MME : mme" ("$PID_MME")" >> $CPU_MEM_UTL_LOG_FILE

  CPU_MEM_DUMP_SESSIOND=$(ps -p $PID_SESSIOND -o %cpu,%mem | awk NR==2)
  echo $CPU_MEM_DUMP_SESSIOND : sessiond" ("$PID_SESSIOND")" >> $CPU_MEM_UTL_LOG_FILE
}

echo " " >> $CPU_MEM_UTL_LOG_FILE
date >> $CPU_MEM_UTL_LOG_FILE
echo "CPU   MEM    PROCESS" >> $CPU_MEM_UTL_LOG_FILE
echo "=========================" >> $CPU_MEM_UTL_LOG_FILE

#Printing for Python Files
print_python_cpu_mem_usage magmad
print_python_cpu_mem_usage subscriberdb
print_python_cpu_mem_usage directoryd
print_python_cpu_mem_usage enodebd
print_python_cpu_mem_usage policydb
print_python_cpu_mem_usage state
print_python_cpu_mem_usage ctraced
print_python_cpu_mem_usage smsd
print_python_cpu_mem_usage eventd
print_python_cpu_mem_usage mobilityd
print_python_cpu_mem_usage pipelined

#Printing for C files
print_c_cpu_mem_usage

echo " ---- Finished Logging ----" >> $CPU_MEM_UTL_LOG_FILE
