# -*- coding: utf-8 -*-

import random


def crossover(G1, G2):
    for i in range(len(G1)):
        if random.random() <= 0.5:
            G1[i], G2[i] = G2[i], G1[i]
    return G1, G2
