# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

class metadataMp3( ):
    def __init__(self, container, *kwargs ):
        self.container = { }
        self.kw = kwargs
        for i in kwargs:
            self.container[i] = container[i] 
        
    def UpdateMetaData(self, metaData, time):
        artist = ''
        album = ''
        stime = "%.2f" % time + "  min"
        title = ''
        try:
            try:
		        artist = metaData.getArtist( )
		        album =  metaData.getAlbum(	)
		        title = metaData.getTitle(	) 
		    except:
		        artist = metaData.artist
		        album =  metaData.album
		        title = metaData.title
		        
		    if artist == '' or artist == ' ':
		        artist = 'Desconocido'
            if album == '' or album == ' ':
		        album = 'Desconocido'
            if title == '' or title == ' ':
		        title = 'Desconocido'   
        except:
            artist = 'Desconocido'
            album = 'Desconocido'
            title = 'Desconocido'
        self.container["artista"].set_text  (artist)
		self.container["album"].set_text	(album)
		self.container["duracion"].set_text	(stime)
		self.container["titulo"].set_text	(title)
