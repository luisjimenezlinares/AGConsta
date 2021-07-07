# -*- coding: utf-8 -*-

import multiprocessing

from deap import base
from deap import creator
from deap import tools

from segmentsf import *

import numpy as np
import random


class AG_segments:
    """
    Clase que contiene la función del algoritmo genético para calcular el centroide de un conjunto de series utilizando como medida de distancia DTW.
    """
    def __init__(self, pop_size=100, ngen=200, cxpb=0.2, mutpb=0.1, batch_evaluate=False, batch_size=0.1, verbose=False, multi_jobs=False):
        """
        :param pop_size: Tamaño de la población.
        :param ngen: Número de generaciones.
        :param cxpb: Probabilidad de cruce.
        :param mutpb: Probabiliadd de mutación.
        :param batch_evaluate: Bool que indica si se realiza evaluacion con subconjuntos o no.
        :param batch_size: Valos de 0 a 1 que indica el porcentaje del conjunto de series con el que se calculará el fitness de los individuos. Solo utilizado en caso de que batch_size sea True.
        :param verbose: Si se mostrarán mensajes o no.
        :param multi_jobs: Si se utilizan todos los núcleos de la CPU disponibles para calcular el fitness de los individuos o no.
        """
        self.pop_size = pop_size
        self.ngen = ngen
        self.cxpb = cxpb
        self.mutpb = mutpb
        self.batch_evaluate = batch_evaluate
        self.batch_size = batch_size
        self.verbose = verbose
        self.multi_jobs = multi_jobs



    def varAnd(self, population, toolbox):
        """
        Función que constituye una parte del algoritmo evolutivo. La población se modifica aplicando, en primer lugar, la función de cruce. Posteriormente se aplica la de mutación. Se devuelve la población modificada.

        :param population: Lista de individuos a variar.
        :param toolbox: Clase que contiene los operadores.
        :return: La población modificada
        """
        offspring = [toolbox.clone(ind) for ind in population]

        # Apply crossover and mutation on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < self.cxpb:
                offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                              offspring[i])
                del offspring[i - 1].fitness.values, offspring[i].fitness.values

        for i in range(len(offspring)):
            if random.random() < self.mutpb:
                offspring[i], = toolbox.mutate(offspring[i])
                del offspring[i].fitness.values

        return offspring



    def eaSimple(self, population, S, toolbox, stats=None, halloffame=None):
        """
        Esquema general de algoritmo genético. Antes de comenzar el proceso evolutivo se realiza una evaluación inicial de los individuos para calcular su fitness. Si la evaluación es con subconjuntos, se determina un subconjunto de S con el que se evaluarán todos los individuos en esta evaluación inicial.

        Una vez finalizada la evaluación final comienza el proceso evolutivo. En primer lugar, se selecciona la descendencia. Después se modifica mediante la función :func:`varAnd`. Finalmente se reevaluan lon individuos nuevos (aquellos que tienen un fitness invalido), en caso de una evaluación sin subconjuntos. En el caso de una evaluación con subconjuntos, se tomarán todos los individuos como si tuvieran fitness invalido para que todos sean reevaluados. Una vez acabado este proceso, comienza la siguiente generación.

        :param population: Lista de individuos de la población de partida.
        :param S: Lista de series de las que se quiere calcular el centroide.
        :param toolbox: Un objeto de la clase :class:`~deap.base.Toolbox` con los operadores registrados.
        :param stats: Un objeto :class:`~deap.tools.Statistics` en el que se almacenan las estadísticas del proceso evolutivo.
        :param halloffame: Un objeto :class:`~deap.tools.HallOfFame` que contendrá los mejores individuos.

        :return La población final
        :return Un objeto de class:`~deap.tools.Logbook` con información del proceso evolutivo.
        """
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        if self.batch_evaluate:
            batch_n = int(self.batch_size*len(S))
            if batch_n < 1:
                batch_n = 1

        if not self.batch_evaluate:
            invalid_ind = [ind for ind in population if not ind.fitness.valid]
            S_selection = S
        else:
            invalid_ind = [ind for ind in population]
            S_selection = random.sample(S, batch_n)

        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind, S_selection)

        if halloffame is not None:
            halloffame.update(population)

        record = stats.compile(population) if stats else {}
        logbook.record(gen=0, nevals=len(invalid_ind), **record)
        if self.verbose:
            print logbook.stream

        # Begin the generational process
        for gen in range(1, self.ngen + 1):
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population))

            # Vary the pool of individuals
            offspring = self.varAnd(offspring, toolbox)

            # Evaluate the individuals with an invalid fitness
            if not self.batch_evaluate:
                invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                S_selection = S
            else:
                invalid_ind = [ind for ind in offspring]
                S_selection = random.sample(S, batch_n)

            for ind in invalid_ind:
                ind.fitness.values = toolbox.evaluate(ind, S_selection)

            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(offspring)

            # Replace the current population by the offspring
            population[:] = offspring

            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            if self.verbose:
                print logbook.stream

        return population, logbook



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
        tournsize = len(self.pop) / 8

        toolbox = base.Toolbox()
        toolbox.register('generate', generate.sample_generate, S=Sn)
        toolbox.register('population', tools.initRepeat, list, toolbox.generate)
        toolbox.register('evaluate', fitness.fitness_dtw)
        toolbox.register('mutate', mutation.mutation, mu=0, sigma=0.03, desp = int(0.04*len(Sn[0])), sigma_extrem = 0.3)
        toolbox.register('mate', crossover.crossover)
        toolbox.register('select', tools.selTournament, tournsize=10)

        return toolbox



    def calculate_centroids(self, S):
        """
        Función que calcula el centroide de un conjunto de series temporales. Primero registra los operadores y posteriormente se realiza el proceso evolutivo.
        :param S: Series de las que se quiere calcular el centroide.

        :returns: El centroide de S
        :returns: El fitness del centroide
        :returns: Un objeto class:`~deap.tools.Logbook` con información del proceso evolutivo.
        """
        if isinstance(S, np.ndarray):
            S = S.tolist()

        NS = normalizacion.Normalize()
        Sn = NS.normalize(S)

        creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
        creator.create('Individual', list, fitness=creator.FitnessMin)

        toolbox = self.register_toolbox(Sn)

        if self.multi_jobs:
            pool = multiprocessing.Pool()
            toolbox.register('map', pool.map)

        pop = toolbox.population(n=self.pop_size)
        hof = tools.HallOfFame(3)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        _, log = self.eaSimple(pop, Sn, toolbox, stats=stats, halloffame=hof)

        C = hof[0]
        C = NS.desnormalize([C])[0]
        fitness_mejor = fitness.fitness_dtw(C, S)[0]

        if self.multi_jobs:
            pool.close()

        return C, fitness_mejor, log



if __name__ == '__main__':
    from read_series import read_series

    S = read_series('../../Datos/aux/50words.csv')
    AG = AG_segments(verbose=True)
    AG.calculate_centroids(S)
