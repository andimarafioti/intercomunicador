# -*- coding: utf-8 -*-
import StringIO
import hashlib
from math import floor
from PySide.QtGui import QPixmap


def transformToLists(*args):
	params = []
	for arg in args:
		if arg is not None and not isinstance(arg, list):
			params.append([arg])
		else:
			params.append(arg)

	return params

def inv_duration(duracion_string):
	l = duracion_string.split(":")
	l.reverse()
	i = 0
	total = 0
	for num in l:
		num = int(num)
		total += num*(60**i)
		i+=1
	return total

def secondsToDuration(seconds):
	minutes = int(floor(seconds / 60))
	seconds = seconds % 60
	return "%d:%02d" % (minutes, seconds)

def numeroATexto(numero):
	if numero < 1000:
		return str(numero)
	elif numero < 1000000:
		return "{}k".format(numero / 1000)
	else:
		return "{}m".format(numero / 1000000)

def segundosAHora(time):
	hor = (int(time / 3600))
	minu = int((time - (hor * 3600)) / 60)
	seg = time - ((hor * 3600) + (minu * 60))
	if seg < 10:
		seg = "0" + str(seg)
	if hor == 0:
		return str(minu) + ":" + str(trunc(seg))
	else:
		return str(hor) + ":" + str(minu) + ":" + str(trunc(seg))

def trunc(seg):
	a = str(seg).split(".")
	return a[0]

def getPixmap(raw_image_data):
	pixmap = QPixmap()
	pixmap.loadFromData(raw_image_data)
	return pixmap

def contarTiempoCanciones(canciones):
	tiempo = 0
	for cancion in canciones:
		tiempo += cancion.duracion
	return tiempo

def segundosAHoras(segundos):
	m, s = divmod(segundos, 60)
	h, m = divmod(m, 60)
	return "%02d:%02d" % (h, m)

def hasNone(list_dict_or_var):
	if list_dict_or_var is None:
		return True
	if isinstance(list_dict_or_var, list):
		if None in list_dict_or_var:
			return True
	if isinstance(list_dict_or_var, dict):
		if None in list_dict_or_var.values():
			return True
	return False

def hashString(string):
	return hashlib.sha256(string).hexdigest()

def obtenerImagenDesdeBinario(dato):
	file_imagen = StringIO.StringIO(dato)
	image_data = file_imagen.getvalue()
	file_imagen.close()
	if image_data == "None":
		image_data = None
	return image_data

def obtenerImagenDesdePath(path):
	file_imagen = StringIO.StringIO(open(path,'rb').read())
	image_data = file_imagen.getvalue()
	file_imagen.close()
	if image_data == "None":
		image_data = None
	return image_data