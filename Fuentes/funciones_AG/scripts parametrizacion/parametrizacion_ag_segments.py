#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 19:41:01 2017

@author: pablo
"""

from __future__ import division

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from read_series import read_series
from tabulate import tabulate

from segmentsf import *

import numpy as np
import random
import matplotlib.pyplot as plt

import multiprocessing

#Parametros fijos
POPULATION = 50

N = len(S)
datasets = ['45_series', '50words', 'gestures', 'medical_images']
#datasets = ['45_series']

generarar = [generate.random_generate, generate.sample_generate]

toolbox = base.Toolbox()

algoritmos = [algorithms.eaSimple, algorithms.eaMuCommaLambda, algorithms.eaMuPlusLambda]
algoritmos_resultados = []
algoritmos_names = ['eaSimple', 'eaMuCommaLambda', 'eaMuPlusLambda']


def main():
    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMin)
    
    for datos in datasets:
        S = read_series('../../Datos/aux/{0}.csv'.format(datos))
        for i, algoritmo in enumerate(algoritmos):
            #Seleccion algoritmo
            print 'Algoritmo[{0}]: {1}'.format(algoritmos_names[i], datos)
            
            toolbox.register('generate', sample_generate, S=S)
            toolbox.register('population', tools.initRepeat, list, toolbox.generate)
            toolbox.register('evaluate', fitness.fitness, S=S)
            toolbox.register('mutate', mutation.mutation, mu=0, sigma=(np.max(S[0])-np.min(S[0]))/np.mean(S[0]), lows=lows, ups=ups, desp = [5, 4, 3, 2, 1, -1, -2, -3, -4, -5])
            toolbox.register('mate', crossover.crossover)
            toolbox.register('select', tools.selTournament, tournsize=10)
            pool = multiprocessing.Pool()
    		toolbox.register('map', pool.map
            
            pop = toolbox.population(n=POPULATION)
            hof = tools.HallOfFame(3)
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("avg", np.mean)
            stats.register("std", np.std)
            stats.register("min", np.min)
            stats.register("max", np.max)
            
            if algoritmos_names[i] == 'eaSimple':
                pop, log = algoritmos[i](pop, toolbox, cxpb=0.2, mutpb=0.1, ngen=50, stats = stats, halloffame=hof, verbose=False)
            elif algoritmos_names[i] == 'eaMuCommaLambda':
                pop, log = algoritmos[i](pop, toolbox, lambda_ = 50, mu = 30, cxpb=0.2, mutpb=0.1, ngen=50, stats = stats, halloffame=hof, verbose=False)
            else:
                pop, log = algoritmos[i](pop, toolbox, lambda_ = 50, mu = 50, cxpb=0.2, mutpb=0.1, ngen=50, stats = stats, halloffame=hof, verbose=False)
        
            print 'Fitness mejor serie: ', hof[0].fitness.values[0]
            algoritmos_resultados.append([algoritmos_names[i], datos, hof[0].fitness.values[0]])
    
    print tabulate(algoritmos_resultados, headers=['Algoritmo', 'Dataset', 'Fitness'])


if __name__ == "__main__":
    main()
