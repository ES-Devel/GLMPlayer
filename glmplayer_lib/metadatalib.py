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
# with this program.  If not, see <http://www.gfrom gi.repository import Gtknu.org/licenses/>.
### END LICENSE

class metadataMp3( ):
    def __init__(self, container, *kwargs ):
        self.container = { }
        self.kw = kwargs
        for i in kwargs:
            self.container[i] = container[i] 
        
    def UpdateMetaData(self, metaData, time):
		self.container["artista"].set_text( metaData.getArtist(	) )
		self.container["album"].set_text	( metaData.getAlbum(	) )
		self.container["duracion"].set_text	( "%.2f" % time + "  min" )
		self.container["titulo"].set_text	( metaData.getTitle(	) )
