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
	
Instalación:
============

	$ python setup.py build 
	# python setup.py install --prefix="PATH1" --root="PATH2" --record uninstallGlmplayer
	
	los valores recomendados para la instalacion son:
		--prefix = "/usr/local"
		--root = "/"
	
	si conoce lo que esta haciendo puede utilizar otros valores
	
	*** 
		La opcion --record proporciona un nombre para un archivo
		donde se almacenan todos los archivos creados durante la 
		instalación, de manera que facilite la desinstalación del 
		programa. Copie este archivo y guardelo en una ubicación
		donde pueda encontrarlo fácilmente. 
		
		El nombre sugerido para este archivo es: uninstallGlmplayer
		sinembargo usted puede darle el nombre que le parezca más
		conveniente, manteniendo un nombre significativo. 
	*** 
		
	para mas informacion
		  $ python setup.py --help
	 
Desinstalación:
===============

	si guardó el archivo uninstallGlmplayer o lo guardo con otro nombre,
	moverse al directorio donde este archivo se encuentre y ejecutar el
	siguiente comando (recuerde que si usó otro nombre de archivo debe
	indicar el nombre usado en lugar del predeterminado):
	
		cat uninstallGlmplayer | xargs rm -rf
	
	revisa el archivo y ten cuidado que no incluya algun nombre como
	/usr/bin/ eso borraría todos los programas de tu ordenador, cada linea
	debe terminar sin '/' lo que indica que solo borará un archivo
		
el archivo glmplayer.desktop:
=============================
	
	por defecto las configuraciones del menú de gnome se guardan en el 
	archivo glmplayer.desktop que después de la instalación se ubica 
	por defecto bajo el directorio /usr/local/share/applications/, la
	ruta completa sería  /usr/local/share/applications/glmplayer.desktop.
	para editar este archivo debes tener permisos de superusuario y abrirlo
	con tu editor favorito. El contenido del archivo por defecto es el siguiente:
	
		[Desktop Entry]
		_Name=Glmplayer
		_Comment=Mp3 Player
		Categories=GNOME;AudioVideo;
		Exec=glmplayer
		Icon=/usr/local/share/glmplayer/media/glmplayer.png
		Terminal=false
		Type=Application
		
	_Name indica el nombre a mostrar en el menú,
	_Comment es el comentario que se muestra al pasar el ratón sobre la entrada del menú
	Categories es la ubicación del programa en el menú según la especificación de gnome
	Exec el nombre del programa
	Icon es la ubicación del icono que se muestra junto al nombre del programa en el menú
	Terminal indica si necesita ejecutarse en un terminal
	Type el tipo de programa distribuido
	
	* Puedes modificar estos parametros para realizar acciones como cambiar de categoría el
	programa o modificar el icono del menu. Agrandar la descripción, o cambiar el nombre del 
	programa a mostrar en el menú 
	
========================================================================
========================================================================
si tiene alguna duda o desea alguna informacion contactar a: 
	William Parras - william.parras.mendez@gmail.com
	EsDevel team -  esdevel@gmail.com
========================================================================
========================================================================
