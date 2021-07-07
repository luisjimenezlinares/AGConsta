# -*- coding: utf-8 -*-

import random


def mutation(G):
    #Muta un 1% de los genes
    genes_a_mutar = []
    genes1p = len(G) / 100
    #Si el 1% es 0, se selecciona un gen al azar
    if genes1p == 0:
        genes_a_mutar = [random.randint(0, len(G)-1)]
    #Sino se selecciona un 1% de los genes
    else:
        genes_a_mutar = random.sample(range(len(G)), genes1p)

    for i in genes_a_mutar:
        gen = G[i]
        c = random.randint(0, len(gen)-1)
        mutado = False

        #Si el alelo seleccionado tiene longitud 1 se prueba a borrar
        if len(gen[c]) == 1:
            if c > 0 and gen[c][0] in gen[c-1]:
                gen.pop(c)
                mutado = True
            elif c < len(gen) - 1 and gen[c][0] in gen[c+1]:
                gen.pop(c)
                mutado = True

        #Si no se ha mutado todavia se une aleatoriamente, en caso de que sea posible, con el alelo de la izquierda o el de la derecha
        if not mutado:
            if random.random < 0.5:
                if c > 0 and not(c > 1 and len(gen[c-1]) == 1 and gen[c-1][0] in gen[c-2]):
                    gen[c] = gen[c-1] + gen[c]
                    gen.pop(c-1)
                    mutado = True
            elif not mutado:
                if c < len(gen) - 1 and not(c < len(gen) - 2 and gen[c+1][0] in gen[c+2]):
                    gen[c] = gen[c] + gen[c+1]
                    gen.pop(c+1)
                    mutado = True

        #Si se ha mutado, se divide aleatoriamente algun alelo en dos
        if mutado:
            c1 = random.randint(0, len(gen)-1)
            if len(gen[c1]) == 1:
                gen = gen[:c1] + [gen[c1]] + gen[c1:]
            else:
                #c2 selecciona en que punto se parte el conjunto
                c2 = random.randint(0, len(gen[c1])-2)
                gen = gen[:c1] + [gen[c1][:c2+1]] + [gen[c1][c2+1:]] + gen[c1+1:]
            G[i] = gen

    return G,
