# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from glmplayer_lib import WindowBase, resources

from gi.repository import Gtk

from xml.dom.minidom import Document

from xml.dom import minidom

import os

try:
	import eyeD3
except ImportError:
	import eyed3 as eyeD3

try:
    from mutagen.mp3 import MP3 
except ImportError:
	pass 
	
filepattern=(("MP3","*.mp3") ,) 

class importWindow(WindowBase.window):

	def __init__(self,builder,parent,File):
	    'constructor'
		WindowBase.window.__init__(self,parent,builder)
		'creates gtk filter'	
		self.filtro=Gtk.FileFilter()
		'xml database file'
		self.XML=File
	
	def OpenDialog(self,widget):
		pattern=(".mp3") 	
		self.filtro.set_name("*.mp3")
		'add filter'
		for name, pattern in filepattern:
 			self.filtro.add_pattern(pattern)
		self.getInstance().add_filter(self.filtro)
		'run window'
		respt=self.getInstance().run()
		self.getInstance().remove_filter(self.filtro)
		'hide window'
		self.Hide_()
	    'open xml database'
		dom = minidom.parse(self.XML)
		'xml root element'
		wml = dom.getElementsByTagName ('glmplayer')
		'window answer ( -5 is ok )'
		if respt == -5:
		    'selected files'
			fileselected=self.getInstance().get_filenames()
			for files in fileselected:
			    'split path and file e.g  /home/user/music/song.mp3 returns dirs=/home/user/music/ and files=song.mp3 '
				(dirs,files)=os.path.split(files)
				nombre=files
				ruta=dirs
				try:
				    try:
		    	        audiofile=eyeD3.load(ruta+"/"+nombre)
		    	        tag=audiofile.tag
		    	    except:
		    	        tag=eyeD3.Tag()
		    	        tag.link(ruta+"/"+nombre)
		    	except:
		    	    tag = None
		    	    'this will register and error MISINGPLUGINS - eyed3' 
		    	try:    
				    audio=MP3(ruta+"/"+nombre)
				except:
				    audio=None
				    'this will register and error MISINGPLUGINS - mutagen'
				'set default values'
				titulo = files
				artista = "Desconocido"
				album = "Desconocido"
				'old and new eyed3 interface'
				try:
				    try:
				
				        if tag.getAlbum( ) != "" and tag.getAlbum( ) != " " and tag.getAlbum( ) != None:
					        album=tag.getAlbum( ) 
					
				        if tag.getArtist( ) != "" and tag.getArtist( ) != " " and tag.getArtist( ) != None:
					        artista=tag.getArtist( )
				
				        if tag.getTitle( ) != "" and tag.getTitle( ) != " " and tag.getTitle( ) != None:
					        titulo=tag.getTitle( )
			        except:
			    
			            if tag.album != "" and tag.album != " " and tag.album != None:
					        album=tag.album 
					
				        if tag.artist != "" and tag.artist != " " and tag.artist != None:
					        artista=tag.artist
				
				        if tag.title != "" and tag.title != " " and tag.title != None:
					        titulo=tag.title
				except:
				    'this will register and error MISINGPLUGINS - eyed3'
				try:	
				    duration=audio.info.length
				    time_=int(duration/60)+float(int((float(duration/60)-int(duration/60))*60))/100
				except:
				    duration=0
				    time_=0	
				'updating gui'
				self.getParent().child["media"].append([titulo,album,artista,str(time_)+" min",nombre,ruta])
				'---------- XML structure  ----------'
				"""  
				<glmplayer>
				    <pista>
				        <title></title>
				        <album></album>
				        <artist></artis>
				        <file></file>
				        <path></path>
				    </pista>
				</glmplayer>
				"""
				'------------------------------------'
				'---------- step 1 ----------'
				"""
				<glmplayer>
				    <pista>
				    </pista>
				</glmplayer>
				"""
				maincard=dom.createElement("pista")
				wml[0].appendChild(maincard)
				'------------------------------------'
				'---------- step 2 ----------'
				"""
				<glmplayer>
				    <pista>
				        <title></title>
				    </pista>
				</glmplayer>
				"""
				title_o=dom.createElement("title")
				maincard.appendChild(title_o)
				title_s=dom.createTextNode(titulo)
				title_o.appendChild(title_s)
				'------------------------------------'
				'---------- step 3 ----------'
				"""
				<glmplayer>
				    <pista>
				        <title></title>
				        <album></album>
				    </pista>
				</glmplayer>
				"""
				album_o=dom.createElement("album")
				maincard.appendChild(album_o)
				album_s=dom.createTextNode(album)
				album_o.appendChild(album_s)
				'------------------------------------'
				'---------- step 4 ----------'
				"""
				<glmplayer>
				    <pista>
				        <title></title>
				        <album></album>
				        <artist></artist>
				    </pista>
				</glmplayer>
				"""
				artist_o=dom.createElement("artist")
				maincard.appendChild(artist_o)
				artist_s=dom.createTextNode(artista)
				artist_o.appendChild(artist_s)
				'------------------------------------'
				'---------- step 5 ----------'
				"""
				<glmplayer>
				    <pista>
				        <title></title>
				        <album></album>
				        <artist></artist>
				        <file></file>
				    </pista>
				</glmplayer>
				"""
				file_o=dom.createElement("file")
				maincard.appendChild(file_o)
				file_s=dom.createTextNode(files)
				file_o.appendChild(file_s)
				'------------------------------------'
				'---------- step 6 ----------'
				"""
				<glmplayer>
				    <pista>
				        <title></title>
				        <album></album>
				        <artist></artist>
				        <file></file>
				        <path></path>
				    </pista>
				</glmplayer>
				"""
				path_o=dom.createElement("path")
				maincard.appendChild(path_o)
				paths=dom.createTextNode(dirs)
				path_o.appendChild(paths)
				'------------------------------------'
			'updating database'	
			xmldocument=open(self.XML,"w")
			dom.writexml(xmldocument)
			xmldocument.close()


	
