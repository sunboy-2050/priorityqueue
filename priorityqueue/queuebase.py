#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://blog.ithomer.net

import Queue

class QueueBase(object):
    
    def __init__(self):
        self.queue = Queue.Queue()
    
    def write(self, message):
        self.queue.put(message)
    
    def read(self):
        return self.queue.get()
    
    def delete(self, msg_id=[]):
        pass