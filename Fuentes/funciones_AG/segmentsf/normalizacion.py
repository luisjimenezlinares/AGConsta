#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 20:38:57 2017

@author: pablo
"""
import numpy as np

class Normalize:
    """
    Clase que normaliza y desnormaliza conjuntos de series temporales. Para la normalización se utiliza la media y la desviación típica de todos los elementos de todas las series.
    """
    def normalize(self, S):
        """
        Función que normaliza un conjunto de series temporales.

        :param S: Conunto de series temporales.

        :return: Conjunto de series temporales normalizadas.
        """
        elements = []
        Sn = []

        for s in S:
            elements.extend(s)

        self.media = np.mean(elements)
        self.std = np.std(elements)

        for s in S:
            sn = []
            for i in range(len(s)):
                sn.append((self.media - s[i]) / self.std)
            Sn.append(sn)

        return Sn



    def desnormalize(self, Sn):
        """
        Función que desnormaliza un conjunto de series temporales, dando como resultado las series temporales originales.

        :param Sn: Conjunto de series temporales normalizadas.

        :return: Conjunto de series temporales desnomalizadas.
        """
        S = []
        for sn in Sn:
            s = []
            for i in range(len(sn)):
                s.append(self.media - self.std * sn[i])
            S.append(s)
        return S



if __name__ == '__main__':
    S = [[2,1,2,6],[3,4,6,8]]
    N = Normalize()

    print 'series:', S
    Sn = N.normalize(S)
    print 'normalizadas:', Sn
    Sd = N.desnormalize(Sn)
    print 'desnormalizadas:', Sd
