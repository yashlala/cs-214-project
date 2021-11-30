#!/usr/bin/env python
import time

def executeSomething():
    print("Hi")
i = 0
while i< 5:
    executeSomething()    
    time.sleep(10)
    i = i+1