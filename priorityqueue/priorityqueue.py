#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://blog.ithomer.net

import logging
import time
import threading

import Queue
import cPickle

import queuebase

class PriorityQueue(queuebase.QueueBase):
    def __init__(self, queuenum=0, refreshtime=0.1, isserial=False, average_message_size=1024, queue_size=4096, thread_safe=True):
        '''
        queuenum        :    队列数量
        refreshtime     :    队列优先级刷新时间间隔
        isserial        :    是否序列化，Ture-序列化; False-不序列化
        thread_safe     :    是否线程安全，Ture-加锁; False-不加锁
        '''
        self.queuenum = queuenum
        self.refreshtime = refreshtime
        self.isserial = isserial
        self.average_message_size = average_message_size
        self.queue_size= queue_size
        self.thread_safe = thread_safe
        
        # init queue list
        self.queue_dict = {}        
        self._init_queue(self.queuenum)
        
        self._refresh_priority_run()
        
        if self.thread_safe:
            self._mutex = threading.Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("init PriorityQueue...")
        pass
    
    def _init_queue(self, queuenum=0):
        for i in range(self.queuenum):
            queue = Queue.Queue()
            self.queue_dict[i] = queue
#             print("%d - %s" % (i, queue))
    
    def _lock(self):
        if self.thread_safe:
            self._mutex.acquire()
            
    def _unlock(self):
        if self.thread_safe:
            self._mutex.release()
            
    def write(self, message, priority_queue_index=0):
        if priority_queue_index >= self.queuenum:
            print("priority_queue_index: %d, queuenum: %d" % (priority_queue_index, self.queuenum))
            exit(0)
            
        self._lock()
        try:
            if self.isserial:
                msg = cPickle.dumps(message, protocol=2)
            else:
                msg = message
            (self.queue_dict[priority_queue_index]).put(msg)
        except Exception, e:
            print e
        finally:
            self._unlock()
    
    def read(self, priority_queue_index=0):
        if priority_queue_index > self.queuenum:
            print("priority_queue_index: %d, queuenum: %d" % (priority_queue_index, self.queuenum))
            exit(0)
            
        self._lock()
        try:
            for i in range(self.queuenum):
                queue = self.queue_dict[i]
                while not queue.empty():
                    if self.isserial:
                        msg = cPickle.loads(queue.get())
                    else:
                        msg = queue.get()
                    return msg
#             return self.queue_dict[priority_queue_index].get()
        finally:
            self._unlock()
    
    # refresh queue level by child-thread
    def _refresh_priority_run(self):
        t = threading.Thread(target=self._refresh_priority) 
        t.start() 
    
    def _refresh_priority(self, flag=True):
        while flag:
            time.sleep(self.refreshtime)
            for i in range(self.queuenum):
                queue = self.queue_dict[i]
                if not queue.empty():
                    queue2 = Queue.Queue()
                    while not queue.empty():
                        if self.isserial:
                            msg = cPickle.loads(queue.get())
                        else:
                            msg = queue.get()
                        if msg is None:
                            continue
                        
                        if(not msg.is_message_expired()):
                            msgmeta = msg.get_message_meta()
                            expiretime_used_global = time.time() - msgmeta.get_timestamp()
                            expiretime_used = time.time() - msgmeta.get_lastrefreshtimestamp()
                            if expiretime_used_global > msgmeta.get_timestamp() / 5:
                                self.queue_dict[0].put(msg)    
                            elif expiretime_used > msgmeta.get_lastfreshexpiretime() / 2 and i > 0:      # refresh to higher level
                                self.queue_dict[i-1].put(msg) 
                                msgmeta.set_lastexpiretime(msgmeta.get_lastfreshexpiretime() / 2)       
                                msgmeta.set_lastrefreshtimestamp(time.time())
                            else:
                                queue2.put(msg)
                    self.queue_dict[i] = queue2
    
    def _block_until_message_available(self, query, polling_interval, polling_timeout):
        current_time = time.time()
        while self.queue_collection.find(query).count() == 0:
            if polling_timeout and (time.time() - current_time) > polling_timeout:
                break
            time.sleep(polling_interval)        
