# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:45:41 2017

@author: pablo
"""

import unittest

from segmentsf.interpolation import interpolate
from segmentsf import *

from deap import creator

import numpy as np



class TestFuncionesAuxAGDef(unittest.TestCase):
    def test_longitud_esperada_interpolate(self):
        """
        Test que comprueba que todas las interpolaciones realizadas acaban
        dando como resultado una serie de la longitud deseada. Se prueba con
        longitudes esperadas de serie de 1 a 100 y series de longitud de 1 a
        200.
        """
        for _ in range(100):
            longitud_esperada = np.random.randint(1, 100)
            serie = np.random.rand(np.random.randint(1, 200))
            longitud_obtenida = len(interpolate(serie, longitud_esperada))

            self.assertEqual(longitud_esperada, longitud_obtenida,
            'Error: Serie obtenida de longitud incorrecta: \
            \n Longitud esperada: {0}, Longitud obtenida: {1}'
            .format(longitud_esperada, longitud_obtenida))


    def test_longitud_minima_esperada_interpolate(self):
        """
        Test que comprueba si el comportamiento de la función de interpolación
        es el deseado cuando la longitud esperada es 1.
        """
        serie = np.random.rand(np.random.randint(1, 30))
        longitud_esperada = 1
        longitud_obtenida = len(interpolate(serie, longitud_esperada))

        self.assertEqual(longitud_esperada, longitud_obtenida,
            'Error: Serie obtenida de longitud incorrecta: \
            \n Longitud esperada: {0}, Longitud obtenida: {1}'
            .format(longitud_esperada, longitud_obtenida))


    def test_serie_de_longitud_minima_interpolate(self):
        """
        Test que comprueba si se realiza correctamente la interpolación
        cuando la serie que se interpola tiene longitud 1.
        """
        serie = [1]
        longitud_esperada = 5
        longitud_obtenida = len(interpolate(serie, longitud_esperada))

        self.assertEqual(longitud_esperada, longitud_obtenida,
            'Error: Serie obtenida de longitud incorrecta: \
            \n Longitud esperada: {0}, Longitud obtenida: {1}'
            .format(longitud_esperada, longitud_obtenida))


    def test_correct_path_dtw(self):
        """
        Test que comprueba que se cumplen las condiciones límite, continuidad,
        monotonia de el alineamiento entre dos series dado por dtw.
        """
        for _ in range(100):
            s
            erie1 = np.random.rand(np.random.randint(1, 100))
            serie2 = np.random.rand(np.random.randint(1, 100))
            dist, D, W = dtw.dtw(serie1, serie2)

            self.assertEqual(0, W[0][0], 'Error: Condición límite inicial \
            incumplida')
            self.assertEqual(0, W[1][0], 'Error: Condición límite inicial \
            incumplida')

            self.assertEqual(len(serie1)-1, W[0][-1], 'Error: Condición límite\
            inicial incumplida')
            self.assertEqual(len(serie2)-1, W[1][-1], 'Error: Condición límite\
            inicial incumplida')

            self.assertTrue((np.unique(W[0]) == np.arange(len(serie1))).all(),
            'Error: Condición de continuidad o monotonia incumplida.')
            self.assertTrue((np.unique(W[1]) == np.arange(len(serie2))).all(),
            'Error: Condición de continuidad o monotonia incumplida.')


    def test_longitud_esperada_crossover(self):
        """Test que comprueba que la longitud de las dos series resultantes del
        crossover tienen la longitud que se espera.
        """
        for _ in range(100):
            longitud = np.random.randint(1, 100)
            serie1 = np.random.rand(longitud)
            serie2 = np.random.rand(longitud)
            result1, result2 = crossover.crossover(serie1, serie2)
            self.assertTrue(len(serie1) == len(serie2) == len(result1) ==
                            len(result2), 'Error: Las series resultantes del \
                            crossover no tienen la misma longitud que sus \
                            progenitores.')


    def test_longitud_esperada_mutacion(self):
        """Test que comprueba que la longitud de la serie resultante de la
        mutación tiene la misma longitud que la serie antes de mutar.
        """
        for _ in range(300):
            serie = np.random.rand(np.random.randint(10, 100)).tolist()
            lows = [x-np.random.rand()*2 for x in serie]
            ups = [x+np.random.rand()*2 for x in serie]
            desp = np.random.randint(1, len(serie)/3-1) 
            result = mutation.mutation(serie, mu=0, sigma=2, lows=lows, ups=ups, desp=desp)
            self.assertEqual(len(serie), len(result), 'Error: La serie \
                             resultante no tiene la longitud esperada.')



if __name__ == '__main__':
    unittest.main()
