# -*- coding: utf-8 -*-

import numpy as np


def interpolate(x, m):
    """
    Función que obtiene una serie de longitud *m* a partir de la serie *x*
    mediante interpolación lineal.

    :param x: Serie a interpolar.
    :param m: Longitude la serie que se desea obtener.

    :return: Serie interpolada de longitud *m*.
    """
    if len(x) == 1:
        return [x[0]] * m
    n = len(x) - 1
    step = n / float(m)
    xs = np.arange(step/2.0, n, step)
    return np.interp(xs, range(len(x)), x).tolist()



if __name__ == '__main__':
    print interpolate([1,2,3,4,5,6,24,14], 5)
    print interpolate([1], 5)
