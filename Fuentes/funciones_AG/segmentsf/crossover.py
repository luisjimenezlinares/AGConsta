# -*- coding: utf-8 -*-

from dtw import dtw
from interpolation import interpolate
import random


def crossover(G1, G2):
    """
    Función que cruza dos individuos. En primer lugar se calculan los segmentos del alineamiento. Después se elige aleatoriamente que secuencia de segmentos se van a cruzar. Finalmente se intercambian interpolando las partes cruzadas para que los individuos resultantes tengan la misma longtitud que la de sus progenitores.

    :param G1: Individuo 1.
    :param G2: Individuo 2.

    :return: Descendiente 1.
    :return: Descendiente 2.
    """

    _, W = dtw(G1, G2)
    W1 = W[0]
    W2 = W[1]
    PCs, pc = [], [0]
    for i in range(1, len(W1)-1):
        #Si viene de la diagonal y entra a recta vertical u horizontal
        if W1[i] != W1[i-1] and W2[i] != W2[i-1] and (W1[i] == W1[i+1] or W2[i] == W2[i+1]):
            if pc:
                PCs.append(pc)
            pc = [i]
        #Si viene de recta vertical y horizontal y entra a la diagonal
        elif W1[i] != W1[i+1] and W2[i] != W2[i+1] and (W1[i] == W1[i-1] or W2[i] == W2[i-1]):
            PCs.append(pc)
            pc = [i]
        else:
            pc.append(i)
    PCs.append(pc + [len(W1)-1])

    c1 = random.randint(0, len(PCs)-1)
    c2 = random.randint(0, len(PCs)-1)
    if c1 > c2:
        c1, c2 = c2, c1

    pi, pf = PCs[c1][0], PCs[c2][-1]
    pi1, pf1 = W1[pi], W1[pf]+1
    pi2, pf2 = W2[pi], W2[pf]+1

    G1[pi1:pf1], G2[pi2:pf2] = interpolate(G2[pi2:pf2], len(G1[pi1:pf1])), interpolate(G1[pi1:pf1], len(G2[pi2:pf2]))

    return G1, G2
