
# coding: utf-8

# In[1]:

from dtw import dtw
from interpolation import interpolate
import random

import matplotlib.pyplot as plt
import numpy as np


# In[2]:

for ii in range(20):
	G1 = [1, 1.2, 1.3, 1.5, 1.77, 1.88, 4, 5, 6,  8, 4.2, 3.5, 3.4, 3.0, 2.8, 2.2, 2.0, 1.5, 2.4, 5.7, 6.7, 4.5, 4.2, 2.5, 2.1, 1.4, 1.2, 1.1, 0.9, 0.8]
	G2 = [1, 0.8, 1,1, 1, 1, 1.1, 1.2, 1.6, 1.7, 1.7, 1.5, 5.2, 7,  7.5, 8, 7, 6.4, 5, 3, 3.0, 2.8, 2.2, 1.5, 2.4, 5.7, 6.7, 4, 3, 2.2]
	
	fig = plt.figure(figsize=(10, 6))
	plt.plot(G1)
	plt.savefig('./cruce/' + str(ii) + '_serie1')
	plt.close()
	
	fig = plt.figure(figsize=(10, 6))
	plt.plot(G2)
	plt.savefig('./cruce/' + str(ii) + '_serie2')
	plt.close()
	# In[3]:

	_, W = dtw(G1, G2)
	W1 = W[0]
	W2 = W[1]
	PCs, pc = [], [0]
	for i in range(1, len(W1)-1):
		#Si viene de la diagonal y entra a recta vertical u horizontal
		if W1[i] != W1[i-1] and W2[i] != W2[i-1] and (W1[i] == W1[i+1] or W2[i] == W2[i+1]):
		    if pc:
		        PCs.append(pc)
		    pc = [i]
		#Si viene de recta vertical y horizontal y entra a la diagonal
		elif W1[i] != W1[i+1] and W2[i] != W2[i+1] and (W1[i] == W1[i-1] or W2[i] == W2[i-1]):
		    PCs.append(pc)
		    pc = [i]
		else:
		    pc.append(i)
	PCs.append(pc + [len(W1)-1])


	# In[4]:

	c1 = random.randint(0, len(PCs)-1)
	c2 = random.randint(0, len(PCs)-1)
	if c1 > c2:
		c1, c2 = c2, c1

	pi, pf = PCs[c1][0], PCs[c2][-1]
	pi1, pf1 = W1[pi], W1[pf]+1
	pi2, pf2 = W2[pi], W2[pf]+1


	# In[5]:

	#Plot alineamiento
	M = np.zeros((len(G1), len(G2)))

	fig = plt.figure(figsize=(7, 7))

	ax = fig.gca()
	ax.set_xticks(np.arange(-0.5, len(G1)-0.5))
	ax.set_yticks(np.arange(-0.5, len(G2)-0.5))
	ax.grid(color='black', linestyle='-', linewidth=1)

	ax.set_xticklabels([])
	ax.set_yticklabels([])

	plt.xlim((-0.45, M.shape[0]-0.5))
	plt.ylim((M.shape[1]-0.5,-0.5))

	plt.imshow(M, cmap='Blues')
	plt.plot(W[0], W[1], linewidth=3, zorder=1)

	for w in PCs:
		x = [W1[x[0]] for x in PCs]
		y = [W2[y[0]] for y in PCs]
		plt.scatter(x, y, c='r', zorder=2)

	plt.savefig('./cruce/' + str(ii) + '_alineamiento')
	plt.close()


	# In[6]:

	#Plot alineamiento con segmento seleccionado

	M = np.zeros((len(G1), len(G2)))

	fig = plt.figure(figsize=(7, 7))

	ax = fig.gca()
	ax.set_xticks(np.arange(-0.5, len(G1)-0.5))
	ax.set_yticks(np.arange(-0.5, len(G2)-0.5))
	ax.grid(color='black', linestyle='-', linewidth=1)

	ax.set_xticklabels([])
	ax.set_yticklabels([])

	plt.xlim((-0.5, M.shape[0]-0.5))
	plt.ylim((M.shape[1]-0.5,-0.5))

	plt.imshow(M, cmap='Blues') 
	plt.plot(W1[pi:pf+2], W2[pi:pf+2], linewidth=3,zorder=2,c='r')
	plt.plot(W1, W2, zorder=1, linewidth=3, c='b')

	print 'Alineamiento con el segmento seleccionado'
	plt.savefig('./cruce/' + str(ii) + '_alineamiento_seccion')
	plt.close()


	# In[7]:

	#Plot series con segmento seleccionado   
	fig = plt.figure(figsize=(10, 6))
	print 'Series con la sección a mutar seleccionada'
	plt.plot(G1, c='b', zorder=1)
	plt.plot(range(pi1,pf1), G1[pi1:pf1], c='r', zorder=2, linewidth=2.2)
	plt.savefig('./cruce/' + str(ii) + '_serie1_seccion')
	plt.close()

	#Plot series con segmento
	fig = plt.figure(figsize=(10, 6))
	plt.plot(G2, c='b', zorder=1)
	plt.plot(range(pi2,pf2), G2[pi2:pf2], c='r', zorder=2, linewidth=2.2)
	plt.savefig('./cruce/' + str(ii) + '_serie2_seccion')
	plt.close()


	# In[8]:

	G1[pi1:pf1], G2[pi2:pf2] = interpolate(G2[pi2:pf2], len(G1[pi1:pf1])), interpolate(G1[pi1:pf1], len(G2[pi2:pf2]))

	print 'Series mutadas'
	fig = plt.figure(figsize=(10, 6))
	plt.plot(G1, c='b', zorder=1)
	plt.plot(range(pi1,pf1), G1[pi1:pf1], c='r', zorder=2, linewidth=2.2)
	plt.savefig('./cruce/' + str(ii) + '_serie1m_seccion')
	plt.close()
	
	
	fig = plt.figure(figsize=(10, 6))
	plt.plot(G2, c='b', zorder=1)
	plt.plot(range(pi2,pf2), G2[pi2:pf2], c='r', zorder=2, linewidth=2.2)
	plt.savefig('./cruce/' + str(ii) + '_serie2m_seccion')
	plt.close()

