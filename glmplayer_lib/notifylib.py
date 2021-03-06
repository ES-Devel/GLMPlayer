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

__status__ = "enable"
__package__ = "GlmplayerNotify"

try:
    from gi.repository import Notify as pynotify

    def notify(title, msg, icon=None):
        if not pynotify.is_initted():
            pynotify.init(title)
            note = pynotify.Notification.new(title, msg, icon)
        note.show()
except:
    __status__ = "disabled"

def getStatus():
    return __status__
    
def getPackageName():
    return __package__
