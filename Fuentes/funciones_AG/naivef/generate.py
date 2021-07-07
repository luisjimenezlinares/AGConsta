# -*- coding: utf-8 -*-

from deap import creator
import numpy as np
import random


def random_generate(L, S):
    ind = []
    mini, maxi = minimo(S), maximo(S)
    for i in range(L):
        ind.append(random.random() * (maxi - mini)  + mini)
    return creator.Individual(ind)


def sample_generate(S):
    return creator.Individual(random.choice(S))



def minimo(S):
    return min(map(min, S))


def maximo(S):
    return max(map(max, S))
