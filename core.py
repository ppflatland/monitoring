# -*- coding: utf-8 -*-
from parser_sanderbase import parser_sanderbase
from test_web_servers import start_test_web_servers
import threading
import time
from threading import Thread


#start_test_web_servers()

# init events
#e1 = threading.Event()
#e2 = threading.Event()


# init thread test_web_servers
t1 = threading.Thread(target=start_test_web_servers)
# init thread tparser_sanderbase
t2 = threading.Thread(target=parser_sanderbase)

# start threads
t1.start()
#time.sleep(2)
t2.start()

t1.join()
t2.join()


'''
def start():
    thr = Thread(target=start_test_web_servers)
    thr.start()
    print("test_web_servers - starting")
    thr = Thread(target=parser_sanderbase)
    thr.start()
    print("parser_sanderbase - starting")
start()



if __name__ == '__main__':
    Process(target=start_test_web_servers).start()
    Process(target=parser_sanderbase).start()
'''
