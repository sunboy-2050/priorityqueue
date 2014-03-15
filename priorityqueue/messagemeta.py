#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://blog.ithomer.net

import time

class MessageMeta(object):

    def __init__(self, routing_key=None, unique_key=None, expiretime=-1.0, isexpired=False, timestamp=time.time()):
        self.routing_key = routing_key
        self.unique_key = unique_key
        self.expiretime = expiretime
        self.isexpired = isexpired
        self.timestamp = timestamp
        self.lastexpiretime = self.expiretime
        self.lastrefreshtimestamp = self.timestamp
        
    def set_routing_key(self, routing_key):
        self.routing_key = routing_key
        
    def get_routing_key(self):
        return self.routing_keyl
        
    def set_unique_key(self, unique_key):
        self.unique_key = unique_key
        
    def get_unique_key(self):
        return self.unique_key
        
    def set_expiretime(self, expiretime):
        self.expiretime = expiretime
        
    def get_expiretime(self):
        return self.expiretime
        
    def set_isexpired(self, isexpired):
        self.isexpired = isexpired
        
    def get_isexpired(self):
        return self.isexpired
        
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
        
    def get_timestamp(self):
        return self.timestamp
    
    def set_lastexpiretime(self, lastexpiretime):
        self.lastexpiretime = lastexpiretime
        
    def get_lastexpiretime(self):
        return self.lastexpiretime
    
    def set_lastrefreshtimestamp(self, lastrefreshtimestamp):
        self.lastrefreshtimestamp = lastrefreshtimestamp
        
    def get_lastrefreshtimestamp(self):
        return self.lastrefreshtimestamp
    
    def get_tostring(self):
        out = "{ \"routing_key\":\"%s\", \"unique_key\":\"%s\", \"expiretime\":%s, \"isexpired\":%s, \"timestamp\":%s, \"lastrefreshtimestamp\":%s }" \
                    % (self.routing_key, self.unique_key, self.expiretime, self.isexpired, self.timestamp, self.lastrefreshtimestamp)
        return out
    
    def print_tostring(self):
        print(self._get_tostring())
        