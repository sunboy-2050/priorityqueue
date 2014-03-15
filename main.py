#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://blog.ithomer.net

import uuid
import time, random, functools
import threading

from priorityqueue.message import Message
from priorityqueue.messagemeta import MessageMeta
from priorityqueue.priorityqueue import PriorityQueue

from conf.config import PRIORITY_QUEUE_NUM as queuenum

def timeit(func):
    @functools.wraps(func)
    def __do__(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print('%s usedtime: %ss' % (func.__name__, time.time() - start))
        return result
    return __do__

@timeit
def test_performance(queuenum=3, refreshtime=0.1, isserial=False, messagenum=100):
    priorityqueue = PriorityQueue(queuenum, refreshtime, isserial)
    
    for i in range(messagenum):
        # message meta
        msgmeta = MessageMeta()
        msgmeta.set_routing_key("123")
        msgmeta.set_unique_key(uuid.uuid4().hex)
        msgmeta.set_expiretime(-1.0)
        msgmeta.set_isexpired(False)   
        msgmeta.set_timestamp(time.time())
        
        # message data
        msgdata = "hello world"     
        _id = 100000 + i
        
        msg = Message(_id, msgdata, msgmeta)
        
        priorityqueue.write(msg, random.randint(0, queuenum-1))
        priorityqueue.write(msg, random.randint(0, queuenum-1))
        
#         print("test_threadId: %s, %d -- queue.set() = %s" % (threading.currentThread().getName(), i, msg.get_tostring()))
        
    msg2 = priorityqueue.read()
    while msg2 is not None:
#         print("test_threadId: %s, %d -- queue.get() = %s" % (threading.currentThread().getName(), i, msg2.get_tostring()))
        msg2 = priorityqueue.read()

if __name__ == "__main__":
    print("10, 0.1, True/False, 1000")
    test_performance(10, 0.1, True, 1000)
    test_performance(10, 0.1, False, 1000)
    
    print("10, 0.1, True/False, 10000")
    test_performance(10, 0.1, True, 10000)
    test_performance(10, 0.1, False, 10000)
    
    print("10, 0.1, True/False, 100000")
    test_performance(10, 0.1, True, 100000)
    test_performance(10, 0.1, False, 100000)
    
    print("10, 0.1, True/False, 1000000")
    test_performance(10, 0.1, True, 1000000)
    test_performance(10, 0.1, False, 1000000)