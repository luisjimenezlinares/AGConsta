from ag_naive import ag_naive
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
    serie, fitness, log = ag_segments(S, verbose=True)
    t2 = time.time()-t1
    
    results.append([datos, fitness, t2])
    
    #Plot de la mejor serie
    plt.plot(serie)
    plt.savefig('./figures/segments/series/{0}'.format('S' + datos))
    plt.close()
    
    #Plot de curva de optimizacion
    evol = [x['min'] for x in log]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_title(datos)
    ax.set_xlabel('generaciones')
    ax.set_ylabel('fitness')
    
    ax.plot(evol)
    fig.savefig('./figures/segments/curvas_fitness/{0}'.format('CF' + datos))
    plt.close()


f = open('./experimentos/experimento_segments.csv', 'w')
csvf = csv.writer(f)
csvf.writerows(results)
f.close()

	
	
