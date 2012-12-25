#!/usr/bin/env python
from gi.repository import Gtk
from multiprocessing import Process
import time


class RepThread(Process):  
    def __init__(self, duration,progressBar,curr):  
        Process.__init__(self)  
        self.duration = duration
        self.curr = curr
        self.progressBar =  progressBar
        self.flag = True
  
    def run(self):
		while (self.curr < self.duration ) and self.flag == True:
			step = 100 / self.duration
			nxt = self.curr * step
			self.progressBar.set_text(str(self.curr))
			time.sleep(1)
			print self.curr
			self.curr = self.curr + 1

    def stop(self):
      	self.flag = False
      	self.curr = 1
      	self.progressBar.set_value(0)

    def pause(self):
    	self.flag = False
    	return self.curr,self.duration

