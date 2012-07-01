#!/user/bin/python

import sys
import os

F_OUT = "stop_system.out"
P_NAME = "main"
P_ID_POS = 1

os.system("ps aux | grep %s > %s" % (P_NAME, F_OUT))
f = open(F_OUT, "r")

content = "whatever"
p_flag = True

while(content != ""):

    content = f.readline()
    if content.find(P_NAME) > -1:
        content = content.split()
        process = P_NAME + ".py"
        if content[len(content)-1] == process:
            os.system("kill -9 %s" % content[P_ID_POS])
            p_flag = False
            print "Proccess Finished!"
            break

if p_flag:
    print "Process not found!"

f.close()
os.system("rm -rf %s" % F_OUT)
