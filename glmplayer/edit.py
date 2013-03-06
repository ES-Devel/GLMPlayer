# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from glmplayer_lib import WindowBase, resources

try:
	import eyeD3
except ImportError:
	import eyed3 as eyeD3

class editWindow( WindowBase.window ):

	def __init__( self,builder,parent,MediaTree,MediaObject):
		WindowBase.window.__init__( self , parent , builder )
		self.Tree=MediaTree
		self.MediaObject=MediaObject
	
	def edicion(self,widget):
	    '(afected_col,id)'
	    try:
            self.getParent(	).child["stock_album"].set_text(self.MediaObject.get_row_value('album','file'))
            self.getParent(	).child["stock_interp"].set_text(self.MediaObject.get_row_value('artist','file'))
            self.getParent(	).child["stock_titulo"].set_text(self.MediaObject.get_row_value('title','file'))
            self.Show_(	)
        except:
            print "Ocurrio un error mientras se editaban las pistas"
	   

	def stop_edicion(self,widget):
		self.Hide_()

	def save(self,widget):
		select=self.Tree.get_selection()
		filepath=resources.on_tree_selection_changed(select)
		try:
            audiofile=eyeD3.load(filepath)
            tag=audiofile.tag
        except:
            tag=eyeD3.Tag()
            tag.link(filepath)
        try:
		    tag.setAlbum(self.getParent().child["stock_album"].get_text())
		    tag.setArtist(self.getParent().child["stock_interp"].get_text())
		    tag.setTitle(self.getParent().child["stock_titulo"].get_text())
        except:
            tag.album=u''+self.getParent().child["stock_album"].get_text()
		    tag.artist=u''+self.getParent().child["stock_interp"].get_text()
		    tag.title=u''+self.getParent().child["stock_titulo"].get_text()
		self.MediaObject.set_row_value('album','file',self.getParent().child["stock_album"].get_text())
		self.MediaObject.set_row_value('title','file',self.getParent().child["stock_titulo"].get_text())
		self.MediaObject.set_row_value('artist','file',self.getParent().child["stock_interp"].get_text()) 
		try:
		    tag.update()
		except:
		    audiofile.tag.save()
		self.Hide_()
