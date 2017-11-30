import os
import re 
import sys
import time
if len(sys.argv) == 2:
    if sys.argv[1] == '-v':
        print('Version: 0.1.0.1 ')
        os._exit(0)
    else:
        print('please input -v')
        os._exit(0)
else:
    pass


if len(sys.argv) <= 3:
    print('the number of parameters is incorrect')
    os._exit(0)
    
if sys.argv[2] != 's_mongodb_keyvalue':
    print('Please enter correct service name')
    os._exit(0)

from MongoDBHandle import MongoDBHandleClass
mongoDBHandle = MongoDBHandleClass()

from ThreadHandle import ThreadHandleClass as threadHandle

def checkip(ip):  
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')  
    if p.match(ip):  
        return True  
    else:  
        return False  
if checkip(sys.argv[1]) == True:
    service = threadHandle(2, "Thread-2", mongoDBHandle, '', sys.argv[1], 41010)
    service.setDaemon(True)
    service.start()
else:
    print("IP is err")
    os._exit(0)

def quit(signum, frame):
    print('will quit...')
    sys.exit()

import signal
while True:
    signal.signal(signal.SIGINT, quit)
    while True:
        time.sleep(2)

