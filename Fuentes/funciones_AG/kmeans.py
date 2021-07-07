#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from ag_segments import AG_segments
from ag_segments_coop import AG_segments_coop
from segmentsf import dtw


class Kmeans:
    """
    Clase que contiene el algoritmo KMeans, que agrupa un conjunto de series temporales en k clusters minimizando la distancia intracluster.

    Presenta una serie de métodos con la misma interfaz que los algoritmos de de scikit-learn.
    """
    def __init__(self, k=10, n_init=10, max_it=5, ag='simple', params_ag = {}, verbose=False):
        """
        :param k: Número de clusters.
        :param n_init: Veces que se repetira el algoritmo utilizando distintas inicializaciones de los centroides.
        :param max_it: Iteraciones que se realizan en cada ejecución del algoritmo.
        :param ag: El algoritmo genético que se utiliza. Puede ser 'simple' o 'coop'.
        :param params_ag: Parametros de algoritmo genético.
        :param verbose: Si se mostrarán mensajes o no.
        """
        self.k = k
        self.n_init = n_init
        self.max_it = max_it
        self.verbose = verbose
        self.clusters = None
        self.ag = ag
        if ag == 'simple':
            self.AG = AG_segments(**params_ag)
        elif ag == 'coop':
            self.AG = AG_segments_coop(**params_ag)



    def fit(self, X):
        """
        Función que ejcuta el algoritmo k-means calculando los centroides con el algoritmo genético.

        :param X: Series temporales.
        """
        n = len(X)
        m = len(X[0])
        best = None

        if not isinstance(X, np.ndarray):
            X = np.array(X)

        lows = np.zeros(len(X))
        ups = np.zeros(len(X))

        for i in range(X.shape[1]):
            lows[i] = np.min(X[:,i])
            ups[i] = np.max(X[:,i])

        for it in range(self.n_init):
            inertias = np.zeros(self.k)

            #Inicializa los centros
            centroids = []
            for _ in range(self.k):
                c = np.zeros(X.shape[1])
                for i in range(X.shape[1]):
                    c[i] = np.random.random()*(ups[i]-lows[i])+lows[i]
                centroids.append(c)

            #Computa el kmeans
            clusters = np.zeros(n)
            temp = set()
            for _ in range(self.max_it):
                #calcula el cluster al que pertenece cada serie
                for i, x in enumerate(X):
                    dists = [dtw.dtw(x, c)[0] for c in centroids]
                    label = np.argmin(dists)
                    clusters[i] = label
                    temp.add(label)
                #recalcula los centros
                for i in temp:
                    mask = clusters == i
                    S = X[mask]
                    c, inertia, _ = self.AG.calculate_centroids(S=S)
                    centroids[i] = c
                    inertias[i] = inertia

                    if self.verbose > 2:
                        self._plot(i, c)
                    if self.verbose > 1:
                        self._print(i, inertia)

                total_inertia = inertias.sum()
                if self.verbose > 0:
                    self._print_it(it, total_inertia)

                if best == None or total_inertia < best:
                    best = total_inertia
                    best_clusters = clusters

        self.labels = best_clusters
        self.inertia = best



    def fit_predict(self, X):
        """
        Función que en primer lugar ejecuta el algotimo k-means y devuelve el cluster al que pertence cada serie.

        :param X: Series temporales.
        """
        self.fit(X)
        return self.labels



    def _print(self, n, inertia):
        print 'Cluster[{0}]: {1}'.format(n, inertia)



    def _print_it(self, n, inertia):
        print 'it:[{0}] Inertia: {1}'.format(n, inertia)
        print '-'*25



    def _plot(self, n, c):
        plt.plot(c)
        plt.title('Centroide {0}'.format(n))
        plt.show()
