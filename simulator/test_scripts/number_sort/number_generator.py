#!/usr/bin/python
import random
import os


afile = open("unsorted.txt", "w" )

for i in range(1000000):
    line = str(random.randint(1, 10000))    
    afile.write(line)    
    afile.write(',')

afile.close()

file_path = 'unsorted.txt'
cmd = "sed -i '$ s/.$//' "+file_path
# print(cmd)
os.system(cmd)
