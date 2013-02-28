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
		    artist = metaData.getArtist( )
		    if artist == '' or artist == ' ':
		        artist = 'Desconocido'
            album =  metaData.getAlbum(	)
            if album == '' or album == ' ':
		        album = 'Desconocido'
            title = metaData.getTitle(	) 
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
