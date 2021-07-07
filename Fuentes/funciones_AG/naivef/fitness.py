# -*- coding: utf-8 -*-

from dtw import dtw

def fitness(C, S):
    fitness = 0
    for s in S:
        fitness += dtw(s, C)[0]**2

    return fitness,
