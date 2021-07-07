# -*- coding: utf-8 -*-

from dtw import dtw


def f(G, S):
    C = []
    for pos in range(len(G[0])):
        suma = 0
        n = 0.0
        for i, gen in enumerate(G):
            for x in gen[pos]:
                suma += S[i][x]
                n += 1
        C.append(suma / n)

    return C


def g(G, S, C):
    fitness = 0
    for i in range(len(S)):
        ngen = [[] for _ in range(len(C))]
        d, W = dtw(C, S[i])
        fitness += d**2
        for wi, wj in zip(*W):
            ngen[wi].append(wj)
        G[i] = ngen
    return fitness


def DBA(G, S):
    C = f(G, S)
    fitness = g(G, S, C)
    return G, fitness
