#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
from ag_segments import AG_segments
from ag_segments_coop import AG_segments_coop
from segmentsf import dtw


class Nmean:
    """
    Clase que contiene el algoritmo Nmean, que clasifica un conjunto de series temporales según cuál sea el centroide de la clase más cercano a cada serie.

    Presenta una serie de métodos con la misma interfaz que los algoritmos de de scikit-learn.
    """
    def __init__(self, ag='simple', params_ag = {}, verbose=0):
        """
        :param ag: El algoritmo genético que se utiliza. Puede ser 'simple' o 'coop'.
        :param params_ag: Parametros de algoritmo genético.
        :param verbose: Si se mostrarán mensajes o no.
        """
        self.verbose = verbose
        self.ag = ag
        if ag == 'simple':
            self.AG = AG_segments(**params_ag)
        elif ag == 'coop':
            self.AG = AG_segments_coop(**params_ag)



    def fit(self, X, y):
        """
        Función que calcula los centroides de cada clase.

        :param X: Series temporales.
        :param y: Clase a la que pertenece cada serie temporal.
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        self.classes = np.unique(y)
        self.centroids = []

        #Calcula el centroide de cada clase
        for i, c in enumerate(self.classes):
            mask = y == c
            S = X[mask]
            centroid, inertia, _ = self.AG.calculate_centroids(S=S)
            self.centroids.append(centroid)

            if self.verbose > 0:
                self._print(i, inertia)



    def predict(self, X):
        """
        Función que calcula la clase a la que pertenece cada serie de un conjunto de series *X*. A cada serie se le asigna la clase del centroide más cercano.

        :param X: Series temporales.
        """
        if not self.centroids:
            raise 'Error: First fit the data'

        if not isinstance(X, np.ndarray):
            X = np.array(X)

        self.labels = np.zeros(len(X))
        for i, x in enumerate(X):
            dists = [dtw.dtw(x, c)[0] for c in self.centroids]
            class_index = np.argmin(dists)
            self.labels[i] = self.classes[class_index]



    def fit_predict(self, X_train, y, X_test):
        """
        Función que calcula los centroides y posteriormente clasifica un conjunto de series. Para ello, llama en primer lugar a :meth:`fit` y después a :meth:`predict`.

        :param X_train: Series temporales de entrenamiento.
        :param y_train: Clase de las series temporales de entrenamiento.
        :param X_test: Series temporales a clasificar.

        :return: Clase de cada serie de X_test
        """
        self.fit(X_train, y)
        return self.predict(X_test)



    def pretrained_predict(self, C, X):
        """
        Función que clasifica las series *X* dados los centroides *C*. Por tanto, en este caso el algorimo no necesita entrenamiento.

        :param C: Centroides de cada clase.
        :param X: Series temporales.

        :return: Clase de cada serie de X.
        """
        self.labels = np.zeros(len(X))

        for i, x in enumerate(X):
            min_d = np.inf
            for j, c in enumerate(C):
                d = dtw.dtw(x, c)[0]
                if d < min_d:
                    min_d = d
                    self.labels[i] = j

        return self.labels



    def fuzzy_predict(self, X):
        """
        Función que clasifica las series de *X* de forma difusa. El resultado será el grado de creencia de la pertenencia a cada clase.

        :param X: Series temporales.

        :return: Pertenencia a cada clase.
        """
        if not self.centroids:
            raise 'Error: First fit the data'

        if not isinstance(X, np.ndarray):
            X = np.array(X)

        self.fuzzy_labels = []
        for x in X:
            dists = [dtw.dtw(x, c)[0] for c in self.centroids]
            total = sum(dists)
            creencias_x = [1-d/total for d in dists]
            total_creen = sum(creencias_x)
            creencias_x_norm = [cree/total_creen for cree in creencias_x]
            self.fuzzy_labels.append(creencias_x_norm)
        self.fuzzy_labels = np.array(self.fuzzy_labels)



    def fit_fuzzy_predict(self, X_train, y, X_test):
        """
        Función que calcula los centroides y posteriormente clasifica un conjunto de series de forma difusa. Para ello, llama en primer lugar a :meth:`fit` y después a :meth:`predict`.

        :param X_train: Series temporales de entrenamiento.
        :param y_train: Clase de las series temporales de entrenamiento.
        :param X_test: Series temporales a clasificar.

        :return: Clase de cada serie de X_test
        """
        self.fit(X_train, y)
        return self.fuzzy_predict(X_test)



    def pretrained_fuzzy_predict(self, C, X):
        """
        Función que realiza una clasificación difusa de las series *X* dados los centroides *C*. Por tanto, en este caso el algorimo no necesita entrenamiento.

        :param C: Centroides de cada clase.
        :param X: Series temporales.

        :return: Clase de cada serie de X.
        """
        self.fuzzy_labels = []
        for x in X:
            dists = [dtw.dtw(x, c)[0] for c in C]
            total = sum(dists)
            creencias_x = [1-d/total for d in dists]
            total_creen = sum(creencias_x)
            creencias_x_norm = [cree/total_creen for cree in creencias_x]
            self.fuzzy_labels.append(creencias_x_norm)
        self.fuzzy_labels = np.array(self.fuzzy_labels)

        return self.fuzzy_labels


    def score(self, X_test, y):
        """
        Función que calcula la exactitud de la clasificación.

        :param X_test: Series a clasificar.
        :param y: Clase de las series a clasificar.

        :return: Exactitud.
        """
        self.predict(X_test)
        return (self.labels == y).sum() / float(y.shape[0])



    def _print(self, n, inertia):
        print 'Class[{0}]: {1}'.format(n, inertia)
        print '-'*25
