#!/usr/bin/env python3 

import sys, os
import subprocess
import shlex


try:
  sys.argv[1]
except:
  print ("usage : %s <ip or host> <ip or host> ... <ip or host>" %(sys.argv[0]))
  sys.exit(0)

a=[]
f=open("map.dot","w")
f.write("Graph Map {\n");

for host in sys.argv[1:]:
  old="Local Network"
  args=["/usr/bin/traceroute","-n",host]
  ps=subprocess.Popen(args, stdout=subprocess.PIPE)
  output = ps.communicate()[0]

  for node in output.splitlines()[1:]:
    node=shlex.split(node[4:].decode("utf-8"))[0]
    if (node != "*"):
      path='"%s" -- "%s"' %(old,node)
      print (path)
      if path not in a:
        f.write("       "+path+"\n")
        a.append(path)
      old=node

f.write ("}");
