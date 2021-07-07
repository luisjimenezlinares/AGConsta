from read_series import read_series
import matplotlib.pyplot as plt
from dtw import dtw


def fitness(C, S):
    fitness = 0
    for s in S:
        fitness += dtw(s, C)[0]

    return fitness


S = read_series('../../../Datos/aux/gestures.csv')
C = []
for i in range(len(S[0])):
    suma = 0
    for s in S:
        suma += s[i]
    C.append(suma / float(len(S)))

print fitness(C, S)

plt.plot(C)
plt.show()
