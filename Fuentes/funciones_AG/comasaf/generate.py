# -*- coding: utf-8 -*-

import random


def generate(L, T):
    S = [range(T)]
    for _ in range(L-1):
        #c1 selecciona que conjunto se parte
        c1 = random.randint(0, len(S)-1)
        if len(S[c1]) == 1:
            S = S[:c1] + [S[c1]] + S[c1:]
        else:
            #c2 selecciona en que punto se parte el conjunto
            c2 = random.randint(0, len(S[c1])-2)
            S = S[:c1] + [S[c1][:c2+1]] + [S[c1][c2+1:]] + S[c1+1:]
    return S
