GLMPlayer
=========

reproductor mp3 codificado en python para sistemas operativos GNU/LINUX
=======================================================================

========================================================================
Licencia:
=========

/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 */

========================================================================

dependencias:
=============
	
	
	Build-Depends: 
		debhelper (>= 8),
 		python (>= 2.6.6-3~),
 		python-distutils-extra (>= 2.10)
	
	mutagen 
		versión que utiliza Glmplayer: http://dl.dropbox.com/u/92395777/mutagen-1.20.tar.gz,
		para mayor información visita la web del autor: http://code.google.com/p/mutagen/ 
	gir1.2-glib-2.0,
 	gir1.2-gtk-3.0,
 	python-gst0.10,
 	python-eyed3,
 	gir1.2-gdkpixbuf-2.0

formatos soportados actualmente:
================================
	MP3
	
Instalacion:
============
	$ python setup.py build 
	# python setup.py install --prefix="PATH" --root="PATH"
	
	los valores recomendados para la instalacion son:
		--prefix = "/usr/local"
		--root = "/"
		
	si conoce lo que esta haciendo puede utilizar otros valores
		
	para mas informacion
		  $ python setup.py --help
	 

========================================================================
========================================================================
si tiene alguna duda o desea alguna informacion contactar a: 
	William Parras - william.parras.mendez@gmail.com
	EsDevel team -  esdevel@gmail.com
========================================================================
========================================================================
