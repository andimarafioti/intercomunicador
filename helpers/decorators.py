# -*- coding: utf-8 -*-
def paramsToLists(f):

	def wrapper(*args, **kwargs):
		params = [args[0]]
		for arg in args[1:]:
			if arg is not None and not isinstance(arg, list):
				params.append([arg])
			else:
				params.append(arg)
				
		for key in kwargs:
			value = kwargs[key]
			if value is not None and not isinstance(value, list):
				kwargs[key] = [kwargs[key]]
		return f(*params, **kwargs)

	wrapper.__name__ = f.__name__
	return wrapper
