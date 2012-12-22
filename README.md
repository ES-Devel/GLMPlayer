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
	mutagen -> Modificar y mostrar metadata como: longitud de archivo,
			   imagen de portada
	gstreamer reproduccion de audio
	Gtk -> Interfaz grafica
	GObject
	Glib
	eyeD3 -> metadata como: titulo, artista, album
	
directorios:
============
	/bin -> contiene el archivo que inicializa el programa
	/glmplayer -> clases de ventana principal
	/glmplayer_lib -> ventanas secundarias
	/help -> utilidades varias
	/data -> 
		/config -> archivo de configuracion
		/plugins -> plugins de reproduccion
		/ui -> archivos de interfaz grafica

Bug's:
======
	Interferencia entre Glib y Gstreamer -> core dump
	Interferencia entre threads y Gtk ->
		Gtk.main() detiene los hilos secundarios del programa

features:
=========
	notificaciones: muestra titulo de la cancion
	caratula de album: muestra la caratula del album
	edicion de pistas: permite modificar la metadata de
					   los archivos de audio

formatos soportados:
====================
	los formatos soportados actualmente con mp3

========================================================================
========================================================================
si tiene alguna duda o desea alguna informacion contactar a: 
	William Parras - william.parras.mendez@gmail.com
	EsDevel team -  esdevel@gmail.com
========================================================================
========================================================================
