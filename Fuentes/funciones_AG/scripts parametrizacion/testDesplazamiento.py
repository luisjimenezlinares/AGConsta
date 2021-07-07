# -*- coding: utf-8 -*-

import multiprocessing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from read_series import read_series

from segmentsf import *

import numpy as np

def register_toolbox(S, p):
	toolbox = base.Toolbox()
	toolbox.register('generate', generate.sample_generate, S=S)
	toolbox.register('population', tools.initRepeat, list, toolbox.generate)
	toolbox.register('evaluate', fitness.fitness_dtw, S=S)
	toolbox.register('mutate', mutation.mutation, mu=0, sigma=0.02, desp = int(0.04*len(S[0])), sigma_extrem = p)
	toolbox.register('mate', crossover.crossover)
	toolbox.register('select', tools.selTournament, tournsize=10)
	return toolbox

def ag_segments(S, verbose=False, multi_jobs=False):
    for p  in [0.005, 0.01, 0.015, 0.02, 0.025, 0.03]:
		POPULATION = 100
		NS = normalizacion.Normalize()
		Sn = NS.normalize(S)

		creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
		creator.create('Individual', list, fitness=creator.FitnessMin)

		toolbox = register_toolbox(Sn, p)
		#pool = multiprocessing.Pool()
		#toolbox.register('map', pool.map)

		pop = toolbox.population(n=POPULATION)
		hof = tools.HallOfFame(3)
		stats = tools.Statistics(lambda ind: ind.fitness.values)
		stats.register("avg", np.mean)
		stats.register("std", np.std)
		stats.register("min", np.min)
		stats.register("max", np.max)
		
		pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.2, mutpb=0.1, ngen=200, stats = stats, halloffame=hof, verbose=verbose)

	   
		C = hof[0]
		C = NS.desnormalize([C])[0]
		fitness_mejor = fitness.fitness_dtw(C, S)[0]
		print p, 'fitness:', fitness_mejor
		
		#pool.close()
    return C, fitness_mejor, log

if __name__ == "__main__":
    datasets = ['lighting', 'medical_images', 'syntetic_control', 'yoga']
    for name in datasets:
    	S = read_series('../../Datos/aux/{0}.csv'.format(name))
    	print name
    	ag_segments(S, verbose=False, multi_jobs=False)

