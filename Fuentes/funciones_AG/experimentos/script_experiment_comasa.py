#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 19:54:00 2017

@author: pablo
"""

from ag_comasa import ag_comasa
from read_series import read_series

import time
import csv
import matplotlib.pyplot as plt


results = [['data', 'fitness', 'time']]
datasets = ['50words', 'adiac', 'cricket', 'earthquakes', 'gestures', 'lighting',\
           'medical_images', 'syntetic_control', 'yoga']
 
                 
for datos in datasets:
    S = read_series('../../Datos/aux/{0}.csv'.format(datos))
    
    t1 = time.time()
    serie, fitness, log = ag_comasa(S, verbose=True, multi_jobs=False)
    t2 = time.time()-t1
    
    results.append([datos, fitness, t2])
    
    #Plot de la mejor serie
    fig, ax = plt.subplots(figsize=(15, 10))
    plt.plot(serie)
    plt.savefig('./figures/comasa/series/{0}'.format('S' + datos))
    plt.close()
    
    #Plot de curva de optimizacion
    evol = [x['min'] for x in log]
    fig, ax = plt.subplots(figsize=(15, 10))
    
    ax.set_title(datos)
    ax.set_xlabel('generaciones')
    ax.set_ylabel('fitness')
    
    ax.plot(evol)
    fig.savefig('./figures/comasa/curvas_fitness/{0}'.format('CF' + datos))
    plt.close()


f = open('experimentos/experimento_comasa.csv', 'w')
csvf = csv.writer(f)
csvf.writerows(results)
f.close()

	
	
