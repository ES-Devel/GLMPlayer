# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from glmplayer_lib import WindowBase

class aboutWindow( WindowBase.window ):

	def __init__(self,builder,parent):
		WindowBase.window.__init__( self , parent , builder )
