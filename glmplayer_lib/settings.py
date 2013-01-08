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

import ConfigParser # modulo para manejar archivos de configuracion

import random # generar numeros aleatorios

class ConfigManager( ):

    def __init__( self, parent ):
    
        self.cfg = ConfigParser.ConfigParser( ) #inicializacion 
        self.parent = parent
        self.path = ""
        
    def setConfigFile( self, filePath):
        # cargamos archivo de configuracion
        # se verifica la relatividad de los directorios
        try: 
            self.path = "/usr/local/share/Glmplayer/config/"+filePath
            self.cfg.read([self.path]) 
        except:
            self.path = "data/config/"+filePath 
            self.cfg.read([self.path])

    def LoadSettings( self ):
        try:
    
		    if int(self.cfg.get("playing seetings","random")) == 0:
			    self.parent.child["random"].set_active(False)
		    else:
		    	self.parent.child["random"].set_active(True)
			
		    if int(self.cfg.get("playing seetings","repeat")) == 0:
		    	self.parent.child["repeat"].set_active(False)
		    else:
			    self.parent.child["repeat"].set_active(True)
	    except ConfigParser.NoSectionError:
	        print "No existe la seccion de configuracion"
			
	def random(self,widget):
	    try:
		    if self.parent.child["random"].get_active( ) == False:
		    	self.cfg.set("playing seetings", "random",0)
			    self.parent.gst_builder.MAPA = range(0,self.parent.TOTAL)
			    select = self.parent.child["arbol_pistas"].get_selection( )
			    (modelo,filas) = select.get_selected_rows( )
			    contador = 0
			    val = 0
			    node = " "
			    for i in filas:
			    	for token in i:
			    		if token == '(' or token == ' ' or token == ',' or token == ')':
			    			pass
			    		else:
			    			node = token
			    	val = int(node)
			    self.parent.gst_builder.current = val + 1
			 
		    else:  
	    		self.cfg.set("playing seetings", "random",1)
		    	self.parent.gst_builder.MAPA = range(0,self.parent.TOTAL)
		    	random.shuffle(self.parent.gst_builder.MAPA)
		    	self.parent.gst_builder.current = 0
	    	f = open(self.path, "w")  
	    	self.cfg.write(f)  
		    f.close()
        except ConfigParser.NoSectionError:
            print "Error al leer la configuracion"
		
	def repeat(self,widget):
	    try:
		    if self.parent.child["repeat"].get_active() == False:
		    	self.cfg.set("playing seetings", "repeat",0)
		    else:  
			    self.cfg.set("playing seetings", "repeat",1)	
		    f = open(self.path, "w")  
		    self.cfg.write(f)  
    		f.close()
    	except ConfigParser.NoSectionError:
    	    print "Error al leer la configuracion"
