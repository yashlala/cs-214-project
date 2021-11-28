import sys
import os
import subprocess
import time
import psutil
import datetime
import pandas as pd
import csv
import matplotlib.pyplot as plt

from cgroups import Cgroup


memory_limits = [100, 250, 500, 750, 1000]
pid_list = []
log = open('log.txt', 'a')
# output = open('output.txt', 'x+')

def run_process(name, limit):
        cg = Cgroup('testing'+str(limit))
        cg.set_memory_limit(limit)
        p = subprocess.Popen(['python3', name],
                 stdout=log,
                 stderr=log,
                 preexec_fn=os.setpgrp )
        PID = p.pid
        cg.add(int(PID))
        print('started ' + name + ' with pid '+ str(PID) + ' and memory '+ str(limit) )
        log_time =0 
        check_page_faults(name, PID, limit, log_time)


def check_pid(pid):        
    proc = psutil.Process(pid)
    if proc.status() == psutil.STATUS_ZOMBIE:
        return False
    else:
        return True

def check_page_faults(name, pid, limit, log_time):
    while (check_pid(pid)):
        incr_time = 1
        # print("a process with pid %d exists" % pid)
        stream = os.popen('cut -d " " -f 10,12 /proc/'+str(pid)+'/stat')
        key = name+":"+str(limit)+":"+str(pid)
        output = name+","+str(limit)+","+str(pid)+","+str(log_time)+","+stream.read().replace(" ",",")
        # print(output)
        write_to_file(key, output)
        log_time = log_time + incr_time 
        time.sleep(incr_time)


def write_to_file(key, output):
    f= open('output.csv', 'a+')    
    # lines = f.readLines()
    # for line in f:
    #     print(key)
    #     if key in line:
    #         # line = line.replace(line, output) 
    #         f.write(line.replace(line, output))
    #         return
    f.writelines(output)


def generate_graph(file_name, process):
    df = pd.read_csv(file_name,header=None) 
    # print (df)    
    fig, ax = plt.subplots()
    for memory, group in df.groupby(df.columns[1]):
        group.plot(x=df.columns[3], y=df.columns[4], ax=ax, label=memory)
    
    plt.title('Graph for ' + process)
    plt.xlabel("Time interval in seconds")
    plt.ylabel("Number of Minor page faults")
    
    plt.show()


def main():
    process = sys.argv[1]
    file_name = 'output.csv'
    if os.path.exists(file_name): os.remove(file_name)
    for memory in memory_limits:
        run_process(process, memory)

    generate_graph(file_name, process)

if __name__ == "__main__":
    main()