# -*- coding: utf-8 -*-

from deap import base
from deap import creator
from deap import tools

from segmentsf import *

import numpy as np
import random


def init_seeds():
    np.random.seed = 2016
    random.seed(2016)


class MaquinaEstados:
    def __init__(self, S, pop, cxpb=0.2, mutpb=0.1, batch_size=1):
        self.S = S
        self.pop = pop
        self.mutpb = mutpb
        self.cxpb = cxpb
        self.batch_n = int(len(S)*batch_size)
        if self.batch_n == 0:
            self.batch_n = 1

        #Atributos que definiran el siguiente estado
        self.progenitores = []
        self.hijos = []
        self.no_mutantes = []
        self.mutantes = []
        self.population = None
        self.fitness = None
        self.media_fitness = None
        self.min_fitness = None
        self.max_fitness = None



    def varAnd(self, population, toolbox):
        offspring = [toolbox.clone(ind) for ind in population]

        for i in range(1, len(offspring), 2):
            if random.random() < self.cxpb:
                self.progenitores.append(offspring[i-1][:])
                self.progenitores.append(offspring[i][:])
                offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                              offspring[i])
                del offspring[i - 1].fitness.values, offspring[i].fitness.values
                self.hijos.append(offspring[i-1][:])
                self.hijos.append(offspring[i][:])

        for i in range(len(offspring)):
            if random.random() < self.mutpb:
                self.no_mutantes.append(offspring[i][:])
                offspring[i], = toolbox.mutate(offspring[i])
                del offspring[i].fitness.values
                self.mutantes.append(offspring[i][:])

        return offspring



    def eaSimpleOneGeneration(self, pop, toolbox, Sn):
        S_selection = random.sample(Sn, self.batch_n)

        for ind in pop:
            ind.fitness.values = toolbox.evaluate(ind, S_selection)

        offspring = toolbox.select(pop, len(pop))
        offspring = self.varAnd(offspring, toolbox)

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind, S_selection)

        return offspring



    def register_toolbox(self, Sn):
        """
        Registra los operadores en el toolbox.
        :param Sn: Series normalizadas de las que se calculará el centroide.

        :return Un objeto :class:`~deap.base.Toolbox` con los operadores registrados.
        """
        #Parametros de mutacion
        mu = 0
        sigma = 0.03
        desp = int(0.04*len(Sn[0]))
        sigma_extrem = 0.3
        if desp < 1:
            desp = 1

        #Parametros de seleccion
        tournsize = len(self.pop) / 7
        toolbox = base.Toolbox()
        toolbox.register('generate', generate.sample_generate, S=Sn)
        toolbox.register('evaluate', fitness.fitness_dtw)
        toolbox.register('mutate', mutation.mutation, mu=mu, sigma=sigma, desp=desp, sigma_extrem = sigma_extrem)
        toolbox.register('mate', crossover.crossover)
        toolbox.register('select', tools.selTournament, tournsize=tournsize)

        return toolbox



    def nextEstado(self):
        if isinstance(self.S, np.ndarray):
            self.S = self.S.tolist()

        NS = normalizacion.Normalize(self.S)
        Sn = NS.normalize(self.S)
        self.pop = NS.normalize(self.pop)

        creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
        creator.create('Individual', list, fitness=creator.FitnessMin)

        toolbox = self.register_toolbox(Sn)

        self.pop = [creator.Individual(ind) for ind in self.pop]

        offspring = self.eaSimpleOneGeneration(self.pop, toolbox, Sn)
        offspring = NS.desnormalize(offspring)

        fitnesses = []

        for ind in offspring:
            fitnesses.append(fitness.fitness_dtw(ind, self.S)[0] / (len(self.S[0]) * len(self.S)))


        mutantes = NS.desnormalize(self.mutantes)
        no_mutantes = NS.desnormalize(self.no_mutantes)
        progenitores = NS.desnormalize(self.progenitores)
        hijos = NS.desnormalize(self.hijos)
        population = offspring
        media_fitness = np.mean(fitnesses)
        min_fitness = min(fitnesses)
        max_fitness = max(fitnesses)
        mejor = population[np.argmin(fitnesses)]

        return {'mutantes':mutantes,
                'no_mutantes':no_mutantes,
                'progenitores':progenitores,
                'hijos':hijos,
                'population':population,
                'fitness':fitnesses,
                'media_fitness':media_fitness,
                'min_fitness':min_fitness,
                'max_fitness':max_fitness,
                'mejor':mejor}



if __name__ == '__main__':
    from read_series import read_series

    S = read_series('../../Datos/aux/45_series.csv')
    pop = [random.choice(S) for _ in range(10)]
    estado = MaquinaEstados(S, pop=pop)
    result = estado.nextEstado()
