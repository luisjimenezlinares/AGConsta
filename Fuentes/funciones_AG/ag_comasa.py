# -*- coding: utf-8 -*-

from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

import multiprocessing

from comasaf import *

import sys

import time
import random
import numpy as np

from sklearn.preprocessing import StandardScaler


class AG_comasa:
    def __init__(self, pop_size=100, ngen=25, cxpb=0.2, DBA=True, verbose=False, multi_jobs=False, save_time=False):
        self.pop_size = pop_size
        self.ngen = ngen
        self.cxpb = cxpb
        self.DBA = DBA
        self.verbose = verbose
        self.multi_jobs = multi_jobs
        self.save_time = save_time



    def varAnd(self, population, toolbox):
        offspring = [toolbox.clone(ind) for ind in population]

        # Apply crossover and mutation on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < self.cxpb:
                offspring[i-1], offspring[i] = toolbox.mate(offspring[i-1], offspring[i])
                del offspring[i-1].fitness.values, offspring[i].fitness.values

        for i in range(len(offspring)):
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

        return offspring



    def addNewIndividuals(self, population, toolbox, Sn):
        #Genera nuevos individuos
        newN = int(0.1 * len(population))
        newIndividuals = toolbox.population(n=newN)

        #Aplica la optimización local

        #Se calcula su fitness
        for i in range(len(newIndividuals)):
            newIndividuals[i], f = toolbox.DBA(newIndividuals[i], Sn)
            newIndividuals[i].fitness.values = f,

        #Se extiene la población
        population.extend(newIndividuals)

        return population



    def ag(self, population, toolbox, stats=None, halloffame=None, Sn=None, S=None):
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        if self.save_time:
            self.timesg = []
            tmedida = 0

        if self.save_time:
            fmejor = np.inf
            for ind in population:
                f = (fitness.fitness(ind, S)[0] / len(S)) / len(S[0])
                if fmejor > f:
                    fmejor = f

            self.timesg.append({'time':0,
                                'fitness':fmejor})
            print '[0]', 't:', 0, 'f:', fmejor

            t1 = time.time()

        # Evaluate the individuals with an invalid fitness
        for i in range(len(population)):
            population[i], f = toolbox.DBA(population[i], Sn)
            population[i].fitness.values = f,

        if halloffame is not None:
            halloffame.update(population)

        record = stats.compile(population) if stats else {}
        logbook.record(gen=0, nevals=self.pop_size, **record)
        if self.verbose:
            print logbook.stream

        #Begin the generational process
        for gen in range(1, self.ngen + 1):

            population = self.addNewIndividuals(population, toolbox, Sn)
            # Select the next generation individuals

            offspring = toolbox.select(population, self.pop_size)

            # Vary the pool of individuals
            offspring = self.varAnd(offspring, toolbox)

            # Evaluate the individuals with an invalid fitness
            for i in range(len(offspring)):
                offspring[i], f = toolbox.DBA(offspring[i], Sn)
                offspring[i].fitness.values = f,

            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(offspring)

            # Replace the current population by the offspring
            population[:] = offspring

            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
            logbook.record(gen=gen, nevals=self.pop_size, **record)
            if self.verbose:
                print logbook.stream

            #Guarda el tiempo transcurrido hasta este punto y el fitness del mejor individuo con el conjunto de series S sin normalizar
            if self.save_time:
                t2 = time.time()
                ind_mejor = toolbox.selBest(population)[0]
                fmejor = (fitness.fitness(ind_mejor, S)[0] / len(S)) / len(S[0])
                #Se actualiza el tiempo acumulado en realizar mediciones
                tmedida += time.time() - t2
                #Se resta el tiempo acumulado en realizar mediciones al tiempo total
                ttotal = time.time() - t1 - tmedida
                self.timesg.append({'time':ttotal,
                                    'fitness':fmejor})
                print '[{0}]'.format(gen), 't:', ttotal, 'f:', fmejor


        return population, logbook



    def register_toolbox(self, S):
        toolbox = base.Toolbox()
        toolbox.register('generate', generate.generate, L=len(S[0]), T=len(S[0]))
        toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.generate, len(S))
        toolbox.register('population', tools.initRepeat, list, toolbox.individual)
        toolbox.register('evaluate', fitness.fitness)
        toolbox.register('mutate', mutation.mutation)
        toolbox.register('mate', crossover.crossover)
        toolbox.register('select', tools.selTournament, tournsize=3)
        toolbox.register('selBest', tools.selBest, k=1)
        toolbox.register('DBA', DBA.DBA)

        return toolbox



    def calculate_centroids(self, S):
        St = np.transpose(S)

        stscaler = StandardScaler()
        Stn = stscaler.fit_transform(St)
        Sn = np.transpose(Stn)

        creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
        creator.create('Individual', list, fitness=creator.FitnessMin)

        toolbox = self.register_toolbox(Sn)

        if self.multi_jobs:
            pool = multiprocessing.Pool()
            toolbox.register('map', pool.map)

        pop = toolbox.population(n=self.pop_size)
        hof = tools.HallOfFame(1)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        pop, log = self.ag(pop, toolbox, stats, hof, Sn, S)

        C = hof[0]
        fitness_mejor = fitness.fitness(C, S)[0]

        C = DBA.f(C, S)

        if self.multi_jobs:
        	pool.close()

        return C, log, fitness_mejor


if __name__ == "__main__":
    from read_series import read_series

    S = read_series('../../Datos/aux/45_series.csv')
    AG = AG_comasa(verbose=True, ngen=5, save_time=True)
    _, fm, _ = AG.calculate_centroids(S)
    print AG.timesg
