python3.8 << END

import psutil
import syslog
import subprocess
import time

def dump_cpu_mem_utils_per_process(*argv):

    with open("/var/core/cpu-mem-log.txt", "a") as f:
        print("        ", file=f)
        print("TIME : ", time.asctime( time.localtime(time.time()) ), file=f)
        print("CPU(%), MEM(%), NAME", file=f)
        print("-------------------------------", file=f)
        for arg in argv:
            child = subprocess.Popen(['pgrep', '-f', arg], stdout=subprocess.PIPE, shell=False)
            proc_id = child.communicate()[0]
            process_info = psutil.Process(int(proc_id.split(b'\n')[0]))
            print("%.2f,  %3.2f,  %s" %
                  (process_info.cpu_percent(interval=0.1),
                   process_info.memory_percent(), arg), file=f)

cpu_values = psutil.cpu_percent(percpu=True,interval=1)
syslog.syslog("---- DUMPING CPU AND MEM % UTILIZATION ----")
syslog.syslog("-- Overall CPU=%s RAM=%3.2f --"% (str(cpu_values), psutil.virtual_memory()[2]))

dump_cpu_mem_utils_per_process(
      "magmad", "subscriberdb", "directoryd",
      "enodebd", "policydb", "state", "ctraced",
      "smsd", "eventd", "mobilityd", "pipelined",
      "mme", "sessiond")
END
