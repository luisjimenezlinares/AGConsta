# -*- coding: utf-8 -*-

from dtw import dtw, fastdtw
import numpy as np

def fitness_fastdtw(C, S, vp=0.01):
    """
    Función que calcula el fitness de un individuo *C*. Para ello, calcula la distancia FastDTW entre *C* y cada serie del conjunto *S*.

    :param C: Individuo.
    :param S: Conjunto de series temporales.
    :param vp: Tamaño de la ventana.

    :return: tupla cuyo único elemento es el fitness de *C*
    """
    fitness = 0
    radio = max(1, int(len(S[0])*vp))
    for s in S:
        fitness += fastdtw(s, C, radius=radio)[0]**2
    return fitness,


def fitness_dtw(C, S):
    """
    Función que calcula el fitness de un individuo *C*. Para ello, calcula la distancia FastDTW entre *C* y cada serie del conjunto *S*.

    :param C: Individuo.
    :param S: Conjunto de series temporales.

    :return: tupla cuyo único elemento es el fitness de *C*
    """
    fitness = 0
    for s in S:
        fitness += dtw(s, C)[0]**2
    return fitness,
