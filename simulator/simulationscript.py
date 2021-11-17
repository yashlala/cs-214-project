import sys
import os
import subprocess
import time
import psutil
import datetime

from cgroups import Cgroup


memory_limits = [100, 250, 500, 750, 1000]
pid_list = []
log = open('log.txt', 'a')
# output = open('output.txt', 'x+')

def run_process(name, limit):
        cg = Cgroup('testing'+str(limit))
        cg.set_memory_limit(limit)
        # p = subprocess.Popen(['python3', name])
        # p = subprocess.Popen(['nohup', 'python3', name, '&&'],
        #          stdout=log,
        #          stderr=log,
        #          preexec_fn=os.setpgrp )
        p = subprocess.Popen(['python3', name],
                 stdout=log,
                 stderr=log,
                 preexec_fn=os.setpgrp )
        PID = p.pid
        cg.add(int(PID))
        print('started ' + name + ' with pid '+ str(PID) + ' and memory '+ str(limit) )
        check_page_faults(name, PID, limit)


def check_pid(pid):        
    proc = psutil.Process(pid)
    if proc.status() == psutil.STATUS_ZOMBIE:
        return False
    else:
        return True

def check_page_faults(name, pid, limit):
    while (check_pid(pid)):
        print("a process with pid %d exists" % pid)
        stream = os.popen('cut -d " " -f 10,12 /proc/'+str(pid)+'/stat')
        key = name+":"+str(limit)+":"+str(pid)
        output = str(datetime.datetime.now().time())+name+":"+str(limit)+":"+str(pid) +" "+stream.read()
        print(output)
        write_to_file(key, output)
        time.sleep(30)


def write_to_file(key, output):
    f= open('output.txt', 'a+')    
    # lines = f.readLines()
    # for line in f:
    #     print(key)
    #     if key in line:
    #         # line = line.replace(line, output) 
    #         f.write(line.replace(line, output))
    #         return
    f.writelines(output)


def main():
    process = sys.argv[1]
    for memory in memory_limits:
        run_process(process, memory)

if __name__ == "__main__":
    main()