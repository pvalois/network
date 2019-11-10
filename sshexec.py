#!/usr/bin/env python3 

import sys
from paramiko import *
from dumper import dump
import getopt

username='root'
password=''
port=22

try:
  opts, remain = getopt.gnu_getopt(sys.argv[1:], "p:u:P:", ["password=","username=","port="])
except getopt.GetoptError as err:
  print (err)
  sys.exit(2)

for opt, optarg in opts:
  if opt in ("-u","--username"): username=str(optarg)
  if opt in ("-p","--password"): password=str(optarg)
  if opt in ("-P","--port"): port=int(optarg)

try:
  hostname=remain[0]
except:
  print ("Usage : %s <hostname or ip> --username=login --password=password --port=port",sys.argv[0])
  sys.exit(0)

print ("Opening ssh://%s@%s:%d" %(username,hostname,port))

client = SSHClient()
client.load_system_host_keys()
client.connect(hostname, port=port, username=username, password=password, timeout=5)

for line in sys.stdin:
  stdin, stdout, stderr = client.exec_command(line)
  print ("> "+line)
  stdout=stdout.readlines()
  for line in stdout:
    print (line, end="")
