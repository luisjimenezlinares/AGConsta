# -*- coding: utf-8 -*-

from deap import creator
import numpy as np
import random


def minimo(S):
    return min(map(min, S))


def maximo(S):
    return max(map(max, S))


def random_generate(L, S):
    """
    Función que genera de forma aleatoria un individuo de longitud *L*.
    :param L: Longitud del individuo a generar.
    :param S: Conjunto de series de las que se quiere calcular el centroide.

    :return: Individuo.
    """
    ind = []
    mini, maxi = minimo(S), maximo(S)
    for i in range(L):
        ind.append(random.random() * (maxi - mini)  + mini)
    return creator.Individual(ind)


def sample_generate(S):
    """
    Función que selecciona de forma aleatoria una serie del conjunto *S*.

    :param S: Conjunto de series de las que se quiere calcular el centroide.

    :return: Individuo.
    """
    return creator.Individual(random.choice(S))
