# -*- coding: utf-8 -*-
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from naivef import *

import numpy as np

import multiprocessing


def register_toolbox(S, mins, maxs):
	toolbox = base.Toolbox()
	toolbox.register('generate', generate.sample_generate, S=S)
	#toolbox.register('generate', generate.random_generate, S=S, L=len(S[0]))
	toolbox.register('population', tools.initRepeat, list, toolbox.generate)
	toolbox.register('evaluate', fitness.fitness, S=S)
	toolbox.register('mutate', tools.mutation.mutGaussian, mu=0, sigma=0.02, indpb=0.1)
	toolbox.register('mate', tools.crossover.cxTwoPoint)
	toolbox.register('select', tools.selTournament, tournsize=10)

	return toolbox


def ag_naive(S, verbose=False, multi_jobs=False):
	POPULATION = 100

        if isinstance(S, np.ndarray):
                S = S.tolist()

	NS = normalizacion.Normalize()
	Sn = NS.normalize(S)

	mins = [min(map(min, Sn))] * len(Sn[0])
	maxs = max(map(max, Sn)) * len(Sn[0])

	creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
	creator.create('Individual', list, fitness=creator.FitnessMin)

	toolbox = register_toolbox(Sn, mins, maxs)

        if multi_jobs:
                pool = multiprocessing.Pool()
                toolbox.register('map', pool.map)

	pop = toolbox.population(n=POPULATION)
	hof = tools.HallOfFame(3)

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", np.mean)
	stats.register("std", np.std)
	stats.register("min", np.min)
	stats.register("max", np.max)

	pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.2, mutpb=0.1, ngen=200, stats=stats, halloffame=hof, verbose=verbose)

	C = hof[0]
	C = NS.desnormalize([C])[0]
	fitness_mejor = fitness.fitness(C, S)[0]

	if multi_jobs:
		pool.close()

    	return C, fitness_mejor, log


if __name__ == "__main__":
    pass
