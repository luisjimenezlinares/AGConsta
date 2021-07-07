# -*- coding: utf-8 -*

from __future__ import division
import numpy as np
import random
from interpolation import interpolate
from deap import creator


def mutation(individual, desp, mu, sigma, sigma_extrem):
    """
    Función que muta un individuo. Contiene tres tipos de mutación, cada una de las cuales con una probabilidad. Las mutaciones son el desplazamiento lateral, el desplazamieno vertical suave y el desplazamiento vertical extremo, con probabilidades de 0.4, 0.4 y 0.2 respectivamente.

    Desplazamiento lateral: Se seleccionan dos segmentos del individuo aleatoriamente. Uno de ellos se estrecha y el otro se ensancha.

    Desplazamiento vertical suave: Se selecciona un segmento y se eleva o se desciende.

    Desplazamiento vertical extremo: Se selecciona un gen del individuo y se eleva o se desciende.

    :param desp: Tamaño máximo del desplazamiento.
    :param mu: Media de la distribución gaussiana de la mutación vertical suave.
    :param sigma: Desviación típica de la distribución gaussiana de la mutación vertical suave.
    :param sigma_extrem: Desviación típica de la distribución gaussiana de la mutación vertical extrema.

    :return: Individuo mutado
    """
    d = random.randint(1, desp) * random.choice([-1, 1])
    p = random.random()
    if len(individual) < 3*abs(d):
        print "Desplazamiento imposible"
    else:
        if p < 0.4:
            ant = individual[:]
            c1 = random.choice(range(0, len(individual)))
            if len(individual[:c1]) > abs(d) and len(individual[c1+1:]) > abs(d):
                set_c2 = range(0, c1-abs(d)) + range(c1+abs(d)+1, len(individual))
                c2 = random.choice(set_c2)
            elif len(individual[:c1]) > abs(d):
                set_c2 = range(abs(d)+1, c1-abs(d))
                c2 = random.choice(set_c2)
            else:
                set_c2 = range(c1+abs(d)+1, len(individual)-abs(d))
                c2 = random.choice(set_c2)

            if c1 > c2:
                c1, c2 = c2, c1

            if len(individual[:c1]) > abs(d) and len(individual[c2:]) > abs(d):
                if random.random() < 0.5:
                    c3 = random.choice(range(0, c1-abs(d)))
                    c4 = random.choice(range(c3+abs(d)+1, c1+1))
                    c1, c2, c3, c4 = c3, c4, c1, c2
                else:
                    c3 = random.choice(range(c2, len(individual)-abs(d)))
                    c4 = random.choice(range(c3+abs(d)+1, len(individual)+1))
            elif len(individual[:c1]) > abs(d):
                c3 = random.choice(range(0, c1-abs(d)))
                c4 = random.choice(range(c3+abs(d)+1, c1+1))
                c1, c2, c3, c4 = c3, c4, c1, c2
            else:
                c3 = random.choice(range(c2, len(individual)-abs(d)))
                c4 = random.choice(range(c3+abs(d)+1, len(individual)+1))

            s1 = individual[:c1]
            s2 = interpolate(individual[c1:c2], len(individual[c1:c2])+d)
            s3 = individual[c2:c3]
            s4 = interpolate(individual[c3:c4], len(individual[c3:c4])-d)
            s5 = individual[c4:]

            individual = s1 + s2 + s3 + s4 + s5
            print 'desp', sum(np.array(individual) - np.array(ant))

        elif p < 0.4:
            ant = individual[:]
            size = len(individual)
            cxpoint1 = random.randint(1, size)
            cxpoint2 = random.randint(1, size - 1)
            if cxpoint2 >= cxpoint1:
                cxpoint2 += 1
            else:
                cxpoint1, cxpoint2 = cxpoint2, cxpoint1

            d = random.gauss(mu, sigma)
            for i in range(cxpoint1, cxpoint2):
                individual[i] = individual[i] + d * (random.random()*0.1 + 0.9)
            print 'elev', sum(np.array(individual) - np.array(ant))

        else:
            c = random.randint(0, len(individual)-1)
            individual[c] = individual[c] + random.gauss(mu, sigma_extrem)

        return creator.Individual(individual),

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    s = [1, 1.2, 1.3, 1.5, 1.77, 1.88, 4, 5, 6,  8, 4.2, 3.5, 3.4, 3.0, 2.8, 2.2, 2.0, 1.5, 2.4, 5.7, 6.7, 4.5, 4.2, 2.5, 2.1, 1.4, 1.2, 1.1, 0.9, 0.8]
    plt.plot(s)
    plt.show()

    for i in range(50):
    	print i
    	sm = mutation(s, mu=0, sigma=0.2, desp=5)
