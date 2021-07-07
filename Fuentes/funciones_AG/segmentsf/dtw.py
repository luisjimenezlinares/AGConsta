# -*- coding: utf-8 -*-

#gcc -o dtwf.so -shared -fPIC dtwf.c

import ctypes
import os


class result(ctypes.Structure):
	"""
	Clase utilizada como wrapper entre la estructura C que devuelve la función fdtw escrita en C y el código en Python.

	Los campos son:
	D: Distancia entre las series.
	w1: Parte del alineamiento de la serie 1 respecto a la serie 2.
	w2: Parte del alineamiento de la serie 2 respecto a la serie 1.
	size: Longitud del alineamiento.
	"""
	_fields_ = [('D', ctypes.c_double),
				('w1', ctypes.POINTER(ctypes.c_int)),
				('w2', ctypes.POINTER(ctypes.c_int)),
				('size', ctypes.c_int)]


dtw_lib = ctypes.cdll.LoadLibrary('./segmentsf/dtwf.so')
dtwf = dtw_lib.dtw
dtwf.restype = result

fastdtwf = dtw_lib.fastdtw
fastdtwf.restype = result

freeptrf = dtw_lib.freeptr
freeptrf.restype = None


def dtw(x, y):
	"""
	Función que calcula la distancia DTW y el alineamiento entre dos series temporales *x* e *y*.

	:param x: Serie temporal.
	:param y: Serie temporal

	:return: Distancia entre las series.
	:return: Alineamiento entre las series.
	"""
	x_arr = (ctypes.c_double * len(x))(*x)
	y_arr = (ctypes.c_double * len(y))(*y)

	x_len = len(x)
	y_len = len(y)

	resultado = dtwf(x_arr, y_arr, x_len, y_len)
	D = resultado.D
	size = resultado.size

	w1, w2 = [], []
	for i in xrange(size):
		w1.append(resultado.w1[i])
		w2.append(resultado.w2[i])

	freeptrf(resultado.w1)
	freeptrf(resultado.w2)

	return D, (w1, w2)


def fastdtw(x, y, radius):
	"""
	Función que calcula la distancia FastDTW y el alineamiento entre dos series temporales *x* e *y*.

	:param x: Serie temporal.
	:param y: Serie temporal

	:return: Distancia entre las series.
	:return: Alineamiento entre las series.
	"""
	x_arr = (ctypes.c_double * len(x))(*x)
	y_arr = (ctypes.c_double * len(y))(*y)

	x_len = len(x)
	y_len = len(y)

	resultado = fastdtwf(x_arr, y_arr, x_len, y_len, radius)
	D = resultado.D
	size = resultado.size

	w1, w2 = [], []
	for i in xrange(size):
		w1.append(resultado.w1[i])
		w2.append(resultado.w2[i])

	freeptrf(resultado.w1)
	freeptrf(resultado.w2)

	return D, (w1, w2)
