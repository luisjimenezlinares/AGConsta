#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:48:10 2017

@author: pablo
"""

import unittest
import numpy as np
from segmentsf import *

class TestDTW(unittest.TestCase):
    def test_distancia(self):
        for _ in range(10):
            lon = int(np.random.random() * 200)
            serie1 = np.random.rand(lon)
            serie2 = np.random.rand(lon)
            
            d1, _ = dtw.dtw(serie1, serie2)
            d2, _ = fastdtw.dtw(serie1, serie2)
            
            self.assertEqual(d1, d2, 'Error: Distancia diferente: ({0}, {1})'.format(d1, d2))
	

    def test_alineamiento(self):
        for _ in range(10):
            lon = int(np.random.random() * 20)
            serie1 = np.random.rand(lon)
            serie2 = np.random.rand(lon)
            
            _, W1 = dtw.dtw(serie1, serie2)
            _, W2 = fastdtw.dtw(serie1, serie2)
            W1 = zip(*W1)
            
            self.assertEqual(W1, W2, 'Error: Alineamiento diferente: ({0}, {1})'.format(W1, W2))

        
        
if __name__ == '__main__':
    unittest.main()
