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

# Degradation Profile = Perform regression on slowdown factors for 10%, 20%, so on. 
# Slowdown Factor = (Time with n% mem on RDMA) / (Time with local mem)
# Time with n% mem on RDMA = Software Time + RDMA Swap Time
# Software Time = Time with Local Mem - Disk Swap Time
# Disk Swap Time = # Page Faults * Disk Fault Latency
# RDMA Swap Time = # Page Faults * RDMA Fault Latency

# Time With Local Mem = We can run the program and time this directly. 
# Disk Fault Latency = The kernel team will output this via debugfs.
# RDMA Fault Latency = Google "RDMA latency". 
# Page Faults = Userspace team will measure this.

# memory_limits = [100, 250, 500, 750, 1000]
memory_fractions = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
total_page_faults = []
# some number from the harry_xu file
disk_fault_latency = 1000

# some number of the internet
rdma_fault_latency  = 2000

# this is in seconds
time_with_local_memory = []

rdma_swap_time = []
disk_swap_time = []
software_time =[]


pid_list = []
log = open('log.txt', 'a')
# output = open('output.txt', 'x+')

def populate_page_faults(file_name, count):
    cmd  = "sed -n -e '$p' "+file_name
    last = subprocess.check_output(cmd, shell=True, text=True)
    print(last)
    fault = int(last.rsplit(',', 1)[1].strip())
    total_page_faults.append(fault)
    time_with_local_memory.append((last.split(",")[3].strip()))

    # if count==1:
        
        # print(time_with_local_memory)



def measure_memory(name):
    p = subprocess.Popen(['python3', name],
                 stdout=log,
                 stderr=log,
                 preexec_fn=os.setpgrp )
    PID = p.pid
    memory_use = psutil.Process(PID).memory_info().rss / 1024 ** 2
    # print(memory_use)
    memory_limits = []
    for frac in memory_fractions:
        memory_limits.append(memory_use * frac)
    return memory_limits


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
    memory_limits = measure_memory(process)
    
    count = 1
    for memory in memory_limits:
        run_process(process, memory)
        populate_page_faults(file_name, count)
        count = count +1
    

    
    for page_fault in total_page_faults:
        rdma_swap_time.append(page_fault*rdma_fault_latency)
        disk_swap_time.append(page_fault*disk_fault_latency)

    for time in disk_swap_time:
        software_time.append(time_with_local_memory - time)



    generate_graph(file_name, process)

if __name__ == "__main__":
    main()