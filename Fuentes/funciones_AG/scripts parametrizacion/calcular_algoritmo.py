from __future__ import division

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from read_series import read_series

from segmentsf import *

import numpy as np
import random

import numpy as np

import multiprocessing
import time
import csv


def register_general_operators(toolbox, S):
    toolbox.register('generate', generate.sample_generate, S=S)
    toolbox.register('population', tools.initRepeat, list, toolbox.generate)
    toolbox.register('mutate', mutation.mutation, mu=0, sigma=0.02, desp = 1, sigma_extrem = 0.1)
    toolbox.register('mate', crossover.crossover)
    toolbox.register('select', tools.selTournament, tournsize=10)
    toolbox.register('evaluate', 
                     fitness.fitness_dtw, 
                     S=S)
    
    
#Parametros fijos
POPULATION = 5#100
GENERACIONES = 2#50
CXPB = 0.2
MUTPB = 0.1
LAMBDA = 3#100
MU = 2#70
datasets = ['50words', 'adiac', 'cricket', 'earthquakes',\
           'electric', 'gestures', 'lighting',\
           'medical_images', 'syntetic_control', 'yoga']

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)


#Seleccion de algoritmo
algoritmos = [algorithms.eaSimple, algorithms.eaMuCommaLambda, algorithms.eaMuPlusLambda]
algoritmos_resultados = []
algoritmos_names = ['eaSimple', 'eaMuCommaLambda', 'eaMuPlusLambda']

toolbox = base.Toolbox()

for rep in range(10):
    for datos in datasets:
        S = read_series('../../Datos/aux/{0}.csv'.format(datos))
		
        NS = normalizacion.Normalize()
        Sn = NS.normalize(S)
		
        register_general_operators(toolbox, Sn)
        
        for i, algoritmo in enumerate(algoritmos):
            pool = multiprocessing.Pool()
            toolbox.register('map', pool.map)
            
            print 'Algoritmo[{0}]: {1}'.format(algoritmos_names[i], datos)     

            pop = toolbox.population(n=POPULATION)
            hof = tools.HallOfFame(3)
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("avg", np.mean)
            stats.register("std", np.std)
            stats.register("min", np.min)
            stats.register("max", np.max)
		    
            t1 = time.time()

            if algoritmos_names[i] == 'eaSimple':
                pop, log = algoritmos[i](pop, 
		                                 toolbox, 
		                                 cxpb=CXPB, 
		                                 mutpb=MUTPB,
		                                 ngen=GENERACIONES, 
		                                 stats = stats, 
		                                 halloffame=hof, 
		                                 verbose=False)
            elif algoritmos_names[i] == 'eaMuCommaLambda':
                pop, log = algoritmos[i](pop, 
		                                 toolbox, 
		                                 lambda_ = LAMBDA, 
		                                 mu = MU, 
		                                 cxpb=CXPB, 
		                                 mutpb=MUTPB, 
		                                 ngen=GENERACIONES, 
		                                 stats = stats, 
		                                 halloffame=hof, 
		                                 verbose=False)
            else:
                pop, log = algoritmos[i](pop, 
		                                 toolbox, 
		                                 lambda_ = LAMBDA, 
		                                 mu = MU, 
		                                 cxpb=CXPB, 
		                                 mutpb=MUTPB, 
		                                 ngen=GENERACIONES, 
		                                 stats = stats, 
		                                 halloffame=hof, 
		                                 verbose=False)
            tfinal = time.time() - t1
		    
            C = hof[0]
            C = NS.desnormalize([C])[0]
            fitness_mejor = fitness.fitness_dtw(C, S)
            print 'Fitness mejor serie: ', fitness_mejor[0]
            algoritmos_resultados.append([algoritmos_names[i], datos, fitness_mejor[0], tfinal])
            
            pool.close()



f = open('algoritmos_medidas.csv', 'w')
csvf =csv.writer(f)
csvf.writerow(['Algoritmo', 'Dataset', 'Fitness', 'Tiempo(s)'])
csvf.writerows(algoritmos_resultados)
