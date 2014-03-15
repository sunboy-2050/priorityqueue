#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://blog.ithomer.net

import time

class Message(object):
    
    def __init__(self, _id=-1, msgdata=None, msgmeta=None):
        self._id = _id
        self.msgmeta = msgmeta      # meta
        self.msgdata = msgdata      # data
        
    def set_message_data(self, msgdata):
        self.msgdata = msgdata
        
    def get_message_data(self):
        return self.msgdata
    
    def set_message_meta(self, msgmeta):
        self.msgmeta = msgmeta
        
    def get_message_meta(self):
        return self.msgmeta
        
    def is_message_expired(self):
        self._check_message_isexpired()
        return self.msgmeta.get_isexpired()
    
    def _check_message_isexpired(self):
        expiretime = self.msgmeta.get_expiretime()
        if ( time.time() - self.msgmeta.get_timestamp() ) > expiretime:
            self.msgmeta.set_isexpired(True)
            
    def get_tostring(self):
        out = "{\"_id\":%d, \"msgdata\":\"%s\", \"msgmeta\":%s}" % (self._id, self.msgdata, self.msgmeta.get_tostring())
        return out
    
    def print_tostring(self):
        print(self.get_tostring())
