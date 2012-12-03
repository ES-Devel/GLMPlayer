#!/usr/bin/env python

import threading
from threading import Thread
import gobject
gobject.threads_init()
import time

class RepThread(threading.Thread):  
    def __init__(self, duration,progressBar,curr):  
        threading.Thread.__init__(self)  
        self.duration = duration
        self.curr = curr
        self.progressBar =  progressBar
        self.flag = True
  
    def run(self): 
    	self.flag = True 
        while (self.curr < self.duration ) and self.flag == True:
        	step = 100 / self.duration
        	nxt = self.curr * step
        	self.progressBar.set_value(nxt)
          	time.sleep(1)
          	self.curr = self.curr + 1

    def stop(self):
      	self.flag = False
      	self.curr = 1
      	self.progressBar.set_value(0)

    def pause(self):
    	self.flag = False
    	return self.curr,self.duration

