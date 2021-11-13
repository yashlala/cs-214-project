import sys
import os
import subprocess
import time

from cgroups import Cgroup

cg = Cgroup('testing')
cg.set_memory_limit(100)
PID = sys.argv[1]

cg.add(int(PID))
print(PID)

memory_limits = [250, 500, 750, 1000]
for limit in memory_limits:
    print("Limit changed to", limit )
    cg.set_memory_limit(limit)
    time.sleep(30)



