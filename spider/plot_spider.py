import pandas as pd
from math import pi
import numpy as np
import matplotlib.pyplot as plt

def plot_spider(path, quality, delta_quality, rebuffering_time, labels):
	savespider = True

	stab = []
	qual = []
	reb = []

	min_qual = 1

	for k in range(0, len(quality)):
		qual.append(np.mean(quality[k]))
		stab.append(np.mean(np.abs(delta_quality[k])))
		reb.append(np.mean(rebuffering_time[k]))
	
	#for i in range(0,len(qual)):
	#	if qual[i] < min_qual:
	#		min_qual = int(qual[i]*100)
		
	print('min_qual')
	print(min_qual)
	print('stab')
	print(stab)
	print('qual')
	print(qual)
	print('reb')
	print(reb)
	
	## creo array di lunghezza variabile in base al numero di alg usati rel_real_stab[] norm_rel_real_stab[] rel_real_qual[] norm_rel_real_qual[] in cui l'indice è l'algoritmo
	rel_stab = []
	rel_qual = []
	rel_reb = []

	for k in range(0, len(quality)):
		rel_stab.append(1/stab[k])
		#rel_qual.append(qual[k])
		rel_qual.append(qual[k]*100)
		temp = 1/reb[k]
		mag = int(temp/100)
		if temp > 100:
			temp = temp/mag
		rel_reb.append(temp)


	print('rel_stab')
	print(rel_stab)
	print('rel_qual')
	print(rel_qual)
	print('rel_reb')
	print(rel_reb)

	player = []
	for k in range(0, len(quality)):
		player.append({'Delta':rel_stab[k], 'Quality':rel_qual[k], 'Freezing':rel_reb[k]})

	#finding index for bitrate-based
	print(labels)

	data = pd.DataFrame(player, index = labels)

	#sono qualità, reb, ...
	Attributes =list(data)
	AttNo = len(Attributes)

	values = []
	angles = []
	for k in range(0, len(quality)):
		temp = data.iloc[k].tolist()
		#print('temp')
		#print(temp)
		#values.append(temp + temp[:1])
		values.append(temp)
		temp = [n / float(AttNo) * 2 * pi for n in range(AttNo)]
		#print('temp')
		#print(temp)
		#angles.append(temp + angles[:1])
		angles.append(temp)

	#Create the chart as before, but with both Ronaldo's and Messi's angles/values
	ax = plt.subplot(111, polar=True)

	print(Attributes)
	plt.xticks(angles[0],Attributes)

	#print('values')
	#print(values)
	#print('angles')
	#print(angles)

	colors = ['b','orange','g','r','violet']

	for k in range(0, len(quality)):
		ax.plot(angles[k], values[k], color=colors[k])
		ax.fill(angles[k], values[k], colors[k], alpha=0.1)

	#Rather than use a title, individual text points are added
	for k in range(0, len(quality)):	
		plt.figtext(0.8,0.9-0.05*k,labels[k],color=colors[k])
	

	if savespider == True:
		plt.savefig(path+'spider_plot.png', bbox_inches='tight')
	else:
		plt.show()	
	