# -*- coding: utf-8 -*-

import multiprocessing

from deap import base
from deap import creator
from deap import tools

from segmentsf import *

import numpy as np
import random

import time

"""
Cambiar dtw para aplicarlo sobre subconjunto **no esta registrada completamente en toolbox**
"""

class AG_segments_coop:
    """
    Clase que contiene la función del algoritmo genético utilizando varias especies para calcular el centroide de un conjunto de series utilizando como medida de distancia DTW.
    """
    def __init__(self, pop_size=100, ngen=200, nespecies=3, ngen_intercambio=20, cxpb=0.2, mutpb=0.1, batch_evaluate=False, batch_size=0.1, verbose=False, multi_jobs=False, save_time=False):
        """
        :param pop_size: Tamaño de la población.
        :param ngen: Número de generaciones.
        :param nespecies: Número de especies.
        :param ngen_intercambio: Generaciones tras las cuáles se intercambiarán los mejores individuos de cada especie.
        :param cxpb: Probabilidad de cruce.
        :param mutpb: Probabiliadd de mutación.
        :param batch_evaluate: Bool que indica si se realiza evaluacion con subconjuntos o no.
        :param batch_size: Valos de 0 a 1 que indica el porcentaje del conjunto de series con el que se calculará el fitness de los individuos. Solo utilizado en caso de que batch_size sea True.
        :param verbose: Si se mostrarán mensajes o no.
        :param multi_jobs: Si se utilizan todos los núcleos de la CPU disponibles para calcular el fitness de los individuos o no.
        """
        self.pop_size = pop_size
        self.ngen = ngen
        self.nespecies = nespecies
        self.ngen_intercambio = ngen_intercambio
        self.cxpb = cxpb
        self.mutpb = mutpb
        self.batch_evaluate = batch_evaluate
        self.batch_size = batch_size
        self.verbose = verbose
        self.multi_jobs = multi_jobs
        self.save_time = save_time



    def varAnd(self, population, toolbox):
        """
        Función que constituye una parte del algoritmo evolutivo. La población se modifica aplicando, en primer lugar, la función de cruce. Posteriormente se aplica la de mutación. Se devuelve la población modificada.

        :param population: Lista de individuos a variar.
        :param toolbox: Clase que contiene los operadores.
        :returns: La población modificada
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



    def eaSimpleCoop(self, S, toolbox, stats=None, halloffame=None, Stime=None,  NS=None):
        """
        Esquema general de algoritmo genético que hace uso de varias especies a lo largo del proceso evolutivo. Cada una de las especies tiene un representante, que es el mejor individuo de esa especie.

        En primer lugar, se varían las especies mediante la función :func:`varAnd`. Después se evaluán los indivudos, utilizando *S* o un subconjunto de *S*. Posteriormente, si el número de la generación es múltiplo de ngen_intercambio, se intercambian los representantes entre las distintas especies.

        :param S: Lista de series de las que se quiere calcular el centroide.
        :param toolbox: Un objeto de la clase :class:`~deap.base.Toolbox` con los operadores registrados.
        :param stats: Un objeto :class:`~deap.tools.Statistics` en el que se almacenan las estadísticas del proceso evolutivo.
        :param halloffame: Un objeto :class:`~deap.tools.HallOfFame` que contendrá los mejores individuos.

        :return La población final
        :return Un objeto de class:`~deap.tools.Logbook` con información del proceso evolutivo.
        """
        logbook = tools.Logbook()
        logbook.header = 'gen', 'species', 'evals', 'std', 'min', 'avg', 'max'


        if self.save_time:
            step = int(0.033 / self.batch_size)
            if step == 0:
                step = 1
            tmedida = 0
            self.timesg = []

        ################################################################
        if self.batch_evaluate:
            t1 = time.time()
            batch_n = int(self.batch_size*len(S))
            if batch_n < 1:
                batch_n = 1

        ################################################################

        g = 0
        #Generacion de las especies
        species = [toolbox.population(self.pop_size) for _ in range(self.nespecies)]

        #Seleccion de los representatnes
        representatives = [random.choice(s) for s in species]

        while g < self.ngen:
            next_repr = [None] * len(species)
            for i, s in enumerate(species):
                #Selecciona la siguiente generacion de individuos
                s = self.varAnd(s, toolbox)

                if not self.batch_evaluate:
                    invalid_ind = [ind for ind in s if not ind.fitness.valid]
                    S_selection = S
                else:
                    invalid_ind = [ind for ind in s]
                    S_selection = random.sample(S, batch_n)

                for ind in invalid_ind:
                    ind.fitness.values = toolbox.evaluate(ind, S_selection)

                record = stats.compile(s)
                logbook.record(gen=g, species=i, evals=len(invalid_ind), **record)

                if self.verbose:
                    print logbook.stream

                if halloffame is not None:
                	halloffame.update(s)

                #Intercambio de representantes
                next_repr[i] = toolbox.selBest(s)[0]
                if g % self.ngen_intercambio == 0:
                    r = representatives[:i] + representatives[i+1:]
                    species[i] = toolbox.select(s, len(s) - len(r))
                    species[i].extend(r)
                else:
                     species[i] = toolbox.select(s, len(s))



            representatives = next_repr
            g += 1

            if self.save_time and g % step == 0:
                t2 = time.time()
                ind_mejor = toolbox.selBest(representatives)[0]
                ind_mejor = NS.desnormalize([ind_mejor])[0]
                fmejor = (fitness.fitness_dtw(ind_mejor, Stime)[0] / len(Stime)) / len(Stime[0])
                #Se actualiza el tiempo acumulado en realizar mediciones
                tmedida += time.time() - t2
                #Se resta el tiempo acumulado en realizar mediciones al tiempo total
                ttotal = time.time() - t1 - tmedida
                self.timesg.append({'time':ttotal,
                                    'fitness':fmejor})
                print '[{0}]'.format(g), 't:', ttotal, 'f:', fmejor



        return species, logbook



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
        tournsize = 6

        toolbox = base.Toolbox()
        toolbox.register('generate', generate.sample_generate, S=Sn)
        toolbox.register('population', tools.initRepeat, list, toolbox.generate)
        toolbox.register('evaluate', fitness.fitness_dtw)
        toolbox.register('mutate', mutation.mutation, mu=0, sigma=0.03, desp = int(0.04*len(Sn[0])), sigma_extrem = 0.3)
        toolbox.register('mate', crossover.crossover)
        toolbox.register('select', tools.selTournament, tournsize=tournsize)
        toolbox.register("selBest", tools.selBest, k=1)

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

        hof = tools.HallOfFame(3)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        _, log = self.eaSimpleCoop(S = Sn,
                                     toolbox = toolbox,
                                     stats = stats,
                                     halloffame=hof,
                                     Stime=S,
                                     NS=NS)

        C = hof[0]
        C = NS.desnormalize([C])[0]
        fitness_mejor = fitness.fitness_dtw(C, S)[0]

        if self.multi_jobs:
            pool.close()

        return C, fitness_mejor, log


if __name__ == "__main__":
    from read_series import read_series

    S = read_series('../../Datos/aux/50words.csv')
    AG = AG_segments_coop(verbose=True,
                          batch_evaluate=True,
                          batch_size=.8)
    AG.calculate_centroids(S)
