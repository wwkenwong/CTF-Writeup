#!/usr/bin/env python
import random
import sys
import os
import time

f = open("flag.txt", "r")
flag = f.read()

print """
Welcome to the flag checking oracle. You can check if your flag is the same as
mine! Previous version has a bug and was already fixed now! Same as before, I 
will not let you to brute force that easily... Enjoy and Wait alone!HAHA!
"""

while 1:
    print "Enter your guess:"
    x = sys.stdin.readline()[:-1]
    match = True
    while(len(x)!=len(flag)):
        print "Wrong! Try again."
        print "Enter your guess:"
        x = sys.stdin.readline()[:-1]
    for i in range(len(x)):
	time.sleep(0.5)
        if x[i] != flag[i]:
            match = False
            print "Wrong! Try again."
            break
    if match == True:
        break

print "Correct!"
