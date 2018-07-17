#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib
#matplotlib.use('Qt4Agg')   # generate postscript output by default

import matplotlib.pyplot as plt
from scipy.io import loadmat
import numpy as np
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

from matplotlib import rc

def plot_spider(path, quality, delta_quality, rebuffering_time, labels):
	#rc('font',**{'family':'serif'})
	#rc('text', setex=True)
	#plt.rcParams.update({'figure.autolayout': True})
	params = {'text.latex.preamble' : [r'\usepackage{amsmath}', r'\usepackage{amssymb}', r'\usepackage{amsfonts}']}
	plt.rcParams.update(params)

	plt.close('all')


	#%%

	en_save = True

	# DIRECTORIES
	base_dir = ''
	OUTPUT_DIR = base_dir+'img/'

	#%% REAL TRACES

	"""

	#### REAL TRACES

	## MPC
	SSIM   - 0.989275138587
	Delta  - 0.00202993824023
	Freeze - 0.0125

	"""
	#average values
	## creo array di lunghezza variabile in base al numero di alg usati real_stab[] real_qual[] norm_reb[] in cui l'indice è l'algoritmo con le medie dei valori
	## ho quality[0] in cui 0 è l'indice dell'algoritmo
	## devo fare la media di quality[0] e così via, cioè ridurre la lista di valori ad uno singolo
	stab = []
	qual = []
	reb = []

	for k in range(0, len(quality)):
		qual.append(np.mean(quality[k]))
		stab.append(np.mean(np.abs(delta_quality[k])))
		reb.append(np.mean(rebuffering_time[k]))

	print('stab')
	print(stab)
	print('qual')
	print(qual)
	print('reb')
	print(reb)

	# real_stab_MPC = 0.00202993824023
	# real_stab_MLP2 = 0.00240502305309
	# real_stab_LSTM = 0.0031728275543418498
	# real_stab_Q = 0.00381803456126

	# real_qual_MPC = 0.989275138587
	# real_qual_MLP2 = 0.990513503669
	# real_qual_LSTM = 0.99049963096968097
	# real_qual_Q = 0.989687889609

	# real_reb_MPC = 0.0125
	# real_reb_MLP2 = 0
	# real_reb_LSTM = 0
	# real_reb_Q = 0

	## END REAL TRACES

	## creo array di lunghezza variabile in base al numero di alg usati rel_real_stab[] norm_rel_real_stab[] rel_real_qual[] norm_rel_real_qual[] in cui l'indice è l'algoritmo
	rel_stab = []
	rel_qual = []
	rel_reb = []
	
	#finding index for bitrate-based
	br_index = 0
	print(labels)
	for k in range(0, len(quality)):
		rel_stab.append(1 / stab[k])
		#rel_qual.append(qual[k])
		rel_qual.append(0.89 - qual[k])
		rel_reb.append(0.0006 - reb[k])
		#rel_reb.append(0.015 - reb[k])
		if labels[k] == 'Bitrate-based\n':
			br_index = k

	print('stab')
	print(rel_stab)
	print('qual')
	print(rel_qual)
	print('reb')
	print(rel_reb)

	norm_rel_stab = []
	norm_rel_qual = []
	norm_rel_reb = []
	
	for k in range(0, len(quality)):
		norm_rel_stab.append(rel_stab[k]/rel_stab[br_index])
		norm_rel_qual.append(rel_qual[k]/rel_qual[br_index])
		norm_rel_reb.append(rel_reb[k]/rel_reb[br_index])

	print('norm_stab')
	print(norm_rel_stab)
	print('norm_qual')
	print(norm_rel_qual)
	print('norm_reb')
	print(norm_rel_reb)

	fig = plt.figure(figsize=(8,6))
	ax = fig.add_subplot(111, projection="polar")

	theta = list(np.arange(3)/float(3)*2.*np.pi)
	theta.append(theta[0])

	# Unitary circle
	r = np.ones(1000)
	t = np.linspace(0,2*np.pi,1000)
	ax.plot(t,r, color='k', linewidth=1)

	for k in range(0, len(quality)):
		data = [norm_rel_qual[k], norm_rel_stab[k], norm_rel_reb[k]]
		data.append(data[0])
		ax.plot(theta, data, linestyle=':', marker="o", markersize=5, label=labels[k])

	## Fix axis
	ax.set_xticks(theta)
	ax.set_xticklabels(["", "", ""])

	#ax.text(-0,0,r'Quality', size=13, bbox=dict(fc='w', ec='w', lw=0, alpha=1))
	#ax.text(0,0,  r'Stability', size=13, bbox=dict(fc='w', ec='w', lw=0, alpha=1))
	#x.text(-4,-6, r'Freezing prevention', size=13, bbox=dict(fc='w', ec='w', lw=0, alpha=1))
	#ax.text(1.7,1.5, r'Bitrate-based reference', size=11)

	ax.text(-0.2,1.15,r'Quality', size=13, bbox=dict(fc='w', ec='w', lw=0, alpha=0.5))
	ax.text(2.2,1.8,  r'Stability', size=13, bbox=dict(fc='w', ec='w', lw=0, alpha=0.5))
	ax.text(3.9,1.65, r'Freezing prevention', size=13, bbox=dict(fc='w', ec='w', lw=0, alpha=0.5))
	ax.text(1.7,1.05, r'Bitrate-based reference', size=11, bbox=dict(fc='w', ec='w', lw=0, alpha=0.5))

	#ax.set_rgrids([0.25,0.5,0.75,1,1.25,1.5], angle=0, size=8)
	ax.set_rgrids([], angle=0, size=8)
	ax.get_xaxis().set_visible(False)

	ax.spines['polar'].set_visible(False)
	    
	ax.legend(loc='upper right', fontsize=30, prop={'weight':'bold', 'size': 13}, bbox_to_anchor=(1.5, 1), markerscale=0)


	## SAVE FIGURE
	if en_save:
	    fig.savefig(path+'spyder_plot.png', bbox_inches = 'tight',pad_inches = 0)
	#    os.system('inkscape --export-eps='+OUTPUT_DIR+figure_name+'.eps '+OUTPUT_DIR+figure_name+'.svg')

# def main():
# 	plot_spider()

# if __name__ == "__main__":
#     main()