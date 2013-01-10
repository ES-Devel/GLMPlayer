# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 <William Parras> <william.parras.mendez@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import threading

import time

class threadhandler(threading.Thread):

    def __init__(self, parent):
        threading.Thread.__init__(self) 
        self.parent = parent
        self.refresh()
    
    def refresh(self):
        self.flag = False
	    self.len = 0
	    self.current = 0
    	self.prov = 0
	    parent.child["bar"].set_value(0)
	    parent.child["tiempo"].set_text("00:00")
	    self.minCt = 0
	    self.curr2 = 0

	
    def run( self ):
        while (self.current < self.len ) and self.flag == True:
	    	step = 96 / self.len
	    	nxt = self.current * step
		    parent.child["bar"].set_value(nxt)
		    parent.child["tiempo"].set_text(self.timeFormat(self.secondToMin(self.curr2)))
		    time.sleep(1)
		    self.current = self.current + 1
		    self.curr2 = self.curr2 + 1
	    if not( self.current < self.len ) and ( self.current != 0 or self.len != 0 ):
	        self.child["handler"].clicked( )
	
    def secondToMin(parent, sec): 
        if sec < 60 :
            return sec
	    else:
	        parent.curr2 = 0
	        parent.minCt = parent.minCt + 1  
	        return sec % 60
	        
    def timeFormat(self, time):
        if time < 10:
	        return "0"+str(self.minCt)+":0"+str(time)
    	else:
	        return "0"+str(self.minCt)+":"+str(time)
