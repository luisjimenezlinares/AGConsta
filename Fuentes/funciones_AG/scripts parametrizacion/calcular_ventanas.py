# -*- coding: utf-8 -*-

from __future__ import division

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from sklearn.preprocessing import StandardScaler

from read_series import read_series
from tabulate import tabulate

from segmentsf import *

import numpy as np
import random
import matplotlib.pyplot as plt

import numpy as np

import multiprocessing
import time
import csv

def varAnd(population, toolbox, cxpb, mutpb):
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring


def eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream

    return population, logbook



def register_general_operators(toolbox, S):
    toolbox.register('generate', generate.sample_generate, S=S)
    toolbox.register('population', tools.initRepeat, list, toolbox.generate)
    toolbox.register('mutate', mutation.mutation, 
                     mu=0, 
                     sigma=0.02, 
                     lows=generate.minimos(S), 
                     ups=generate.maximos(S), 
                     desp = int(len(S[0]) * 0.1))
    toolbox.register('mate', crossover.crossover)
    toolbox.register('select', tools.selTournament, tournsize=6)
    
    #pool = multiprocessing.Pool()
    #toolbox.register('map', pool.map)


ss = StandardScaler()

#Parametros fijos
POPULATION = 70
GENERACIONES = 50
CXPB = 0.2
MUTPB = 0.1
datasets = ['ecg_five_days_df', '50words', 'medical_images', 'adiac', 'gestures', 'cricket']

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)


#Seleccion de ventana de DTW
#Los % de radio mas pequenos tendran el mismo efecto en 45 series, 
#porque la ventana sera demasiado pequeña
ventanas = [.01, .02, .03, .04, .05, .06, .07, .08, .09, .1]
ventanas_resultados = []
ventanas_names = map(lambda x: str(x)+'%', ventanas)

toolbox = base.Toolbox()
for datos in datasets:
    S = read_series('../../Datos/aux/{0}.csv'.format(datos))
    S_norm = ss.fit_transform(S)
    register_general_operators(toolbox, S_norm)
    for i, ventana in enumerate(ventanas):
        toolbox.register('evaluate', 
                         fitness.fitness_fastdtw, 
                         S=S_norm, 
                         vp=ventana)
        hof = tools.HallOfFame(1)
        pop = toolbox.population(n=POPULATION)
        
        t1 = time.time()
        pop, log = eaSimple(pop, 
                            toolbox, 
                            cxpb=CXPB, 
                            mutpb=MUTPB, 
                            ngen=GENERACIONES, 
                            stats = None, 
                            halloffame=hof, verbose=False)
        tfinal = time.time() - t1
        C = hof[0]
        C = ss.inverse_transform(hof[0])
        fitness_mejor = fitness.fitness_dtw(C, S)[0]
        print 'Fitness mejor serie[{0}][{1}]: '.format(datos, ventanas_names[i]), fitness_mejor
        ventanas_resultados.append([ventanas_names[i], datos, fitness_mejor, tfinal])

f = open('ventana_medidas.csv', 'w')
csvf =csv.writer(f)
csvf.writerow(['Ventana', 'Dataset', 'Fitness', 'Tiempo(s)'])
csvf.writerows(ventanas_resultados)
