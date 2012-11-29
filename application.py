#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""copyright (c) 2012 - EsDevel"""

import wx
import engine
        
if __name__=='__main__':
    wxObject = wx.App()
    application = engine.main()
    application.run()
    application.build()
    application.__instance__.Show()
    wxObject.MainLoop()