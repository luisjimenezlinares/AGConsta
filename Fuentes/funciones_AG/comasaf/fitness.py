# -*- coding: utf-8 -*-

from dtw import dtw
from DBA import f


def fitness(G, S):
    C = f(G, S)
    fitness = 0
    for s in S:
        fitness += dtw(s, C)[0]**2
    return fitness,

