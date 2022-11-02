# Magma Specific Debugging

## GENERAL DEBUGGING
### G.1 Capturing the regular logs
    -> /var/log/mme.log
    -> /var/log/syslog

### G.2 Use the Cronjobs for cleaning up the log & core files
     https://github.com/wavelabsai/magma-general-utility -> bigfilescleanup
     https://github.com/wavelabsai/magma-general-utility/blob/master/cron-job-steps
     
### G.3 Use the Cronjobs for monitoring CPU and MEMORY
     https://github.com/wavelabsai/magma-general-utility -> cpumemmonitor 
     https://github.com/wavelabsai/magma-general-utility/blob/master/cron-job-steps

### G.4 Default logging level can be changed in inidividual YAML files.
     Ensure the default value of logging is set to "INFO"

## FASTPATH DEBUGGING
### F.1 Additional debugging (Disruptive)
   - Setting flags
      ```
      vagrant@magma-dev:~$ cat /etc/magma/pipelined.yml | grep print_grpc
          magma_print_grpc_payload: true     <<<<<<<<<< By default is false
          vagrant@magma-dev:~$
       ```

   - Restarting the services
        sudo service magma@* stop
        sudo service magma@magmad start
      
   - All the logs will be captured in syslogs
      
   - Once the test is complete we need to turn the flag to false "magma_print_grpc_payload: false"
    
### F.2 Output of fastpath (can do before and after sending traffic)
   - pipelined_cli.py  debug table_assignment
   - sudo ovs-vsctl show
   - sudo ovs-ofctl dump-flows gtp_br0 table=0
   - sudo ovs-ofctl dump-flows gtp_br0 table=12
   - sudo ovs-ofctl dump-flows gtp_br0 table=13
   - sudo ovs-ofctl dump-flows gtp_br0 table=14
   - sudo ovs-ofctl dump-flows gtp_br0 table=20
   - Trace Live Flows :
        sudo ovs-appctl ofproto/trace gtp_br0 in_port=gtp0
   - Trace commands :
        sudo ovs-appctl bridge/dump-flows gtp_br0

### F.3 OVS Upgrades or Re-Install
   - /usr/local/bin/ovs-kmod-upgrade.sh

## CRASH DEBUGGING
### CD.1 In case of crash the information is stored in 
     - cd /var/core
     - ls -> core-1667048239-TASK_S1AP-90557.tgz

