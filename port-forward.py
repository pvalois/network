#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tcp Port Forwarding (Reverse Proxy)
# Author : WangYihang <wangyihanger@gmail.com>
# Update : Pascal valois <pvalois@hotmail.fr> 
#          Cleaning code of uninterresting parties, normalizing input. 

import socket
import threading
import sys

def handle(buffer):
  return buffer

def transfer(src, dst, direction):
  src_name = src.getsockname()
  src_address = src_name[0]
  src_port = src_name[1]
  dst_name = dst.getsockname()
  dst_address = dst_name[0]
  dst_port = dst_name[1]

  while True:
    buffer = src.recv(0x400)
    if len(buffer) == 0: break
    dst.send(handle(buffer))

  src.close()
  dst.close()

def server(local_host, local_port, remote_host, remote_port, max_connection):
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((local_host, local_port))
  server_socket.listen(max_connection)

  while True:
    local_socket, local_address = server_socket.accept()
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    s = threading.Thread(target=transfer, 
                         args=(remote_socket, local_socket, False))
    r = threading.Thread(target=transfer, 
                         args=(local_socket, remote_socket, True))
    s.start()
    r.start()

  #remote_socket.shutdown(socket.SHUT_RDWR)
  remote_socket.close()
  #local_socket.shutdown(socket.SHUT_RDWR)
  local_socket.close()
  #server_socket.shutdown(socket.SHUT_RDWR)
  server_socket.close()

def main():
  if len(sys.argv) != 3:
    print ("Usage : ")
    print ("\t %s ip:port targetip:targetport" % (sys.argv[0]))
    print ("Example : ")
    print ("\t %s 0.0.0.0:5000 10.1.250.18:5000" % (sys.argv[0]))
    exit(1)

  src = sys.argv[1]
  dst = sys.argv[2]

  (localip,localport)=src.split(":")
  (targetip,targetport)=dst.split(":")
  maxconn = 0x10

  print ("enabling forwarding from %s to %s" %(src,dst))
  server(localip,int(localport),targetip,int(targetport),maxconn)

if __name__ == "__main__":
  main()

