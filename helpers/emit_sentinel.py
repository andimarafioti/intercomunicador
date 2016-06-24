# -*- coding: utf-8 -*-
# USO:
# En la definicion del Signal todos los parametros deben ser de tipo object
# En la llamada a un emit sospechoso se debe encerrar a los parametros con pyside_none_wrap
# Ejemplo: SetEstado.emit(estado) ---> SetEstado.emit(*pyside_none_wrap(estado))
# La funcion a la que llama el emit se la debe decorar con pyside_none_deco

import os
from globVars import LOG_ROOT_PATH

_PYSIDE_NONE_SENTINEL = object()

def pyside_none_wrap(*args):
	new_args = map(_sentinel_init, args)
	return new_args

def pyside_none_deco(func):
	def inner(*args, **kwargs):
		for i, arg in enumerate(args):
			if arg == _PYSIDE_NONE_SENTINEL:
				_write_to_file(func, i)
		newargs = map(_sentinel_guard, args)
		newkwargs = {k: _sentinel_guard(v) for k, v in kwargs.iteritems()}
		return func(*newargs, **newkwargs)
	return inner

def _sentinel_init(arg):
	if arg is None:
		return _PYSIDE_NONE_SENTINEL
	return arg

def _sentinel_guard(arg):
	if arg is _PYSIDE_NONE_SENTINEL:
		return None
	return arg

def _write_to_file(func, i):
	f = open(os.path.join(LOG_ROOT_PATH, 'signal_errors.txt'), 'a')
	f.write("Funcion: {}, Arg: {}\n".format(func.__name__, i))
	f.close()


