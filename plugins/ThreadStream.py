#!/usr/bin/env python
import threading
import time


class RepThread(threading.Thread):  
    def __init__(self, duration,progressBar,curr):  
        threading.Thread.__init__(self)  
        self.duration = duration
        self.curr = curr
        self.progressBar =  progressBar
        self.flag = True
  
    def run(self):
		for i in range(0,10):
			print i
			time.sleep(1)
		#self.flag = True
		#while (self.curr < self.duration ) and self.flag == True:
		#	step = 100 / self.duration
		#	nxt = self.curr * step
		#	self.progressBar.set_value(nxt)
		#	time.sleep(1)
		#	self.curr = self.curr + 1

    def stop(self):
      	self.flag = False
      	self.curr = 1
      	self.progressBar.set_value(0)

    def pause(self):
    	self.flag = False
    	return self.curr,self.duration

