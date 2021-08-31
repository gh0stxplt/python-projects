# Author: gh0stxplt
#
# Date: 08/13/2021
#
# Hard coded to scan first ports 1000,
# planning to change this to take args
#
# !/usr/bin/env python3

import sys
import socket
import threading
import time
from queue import Queue

print_lock = threading.Lock()

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])
    print("-" * 40)
    print("\tScanning first 1000 ports\n   Closed ports will not be verbosed")
    print("-" * 40)
    start=time.time()

else:
    print("No IP to scan provided.")
    print("Usage: python3 portscan.py <ip>")
    sys.exit(1)

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        with print_lock:
            print('Port: ' + str(port) + ' is open')
        con.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        scan(worker)
        q.task_done()

q = Queue()

for x in range(150):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(1, 1000):
    q.put(worker)

q.join()

print('Execution time:', round(time.time() - start,2), 'seconds')
