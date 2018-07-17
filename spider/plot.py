# -*- coding: utf-8 -*- 
import re
from array import array
import matplotlib.pyplot as plt
import os
from plot_spider import plot_spider

def main_script(subfolder, test_number):
	path = os.path.join(subfolder, test_number)

	savefigs = False
	savespider = True

	labelsize = 12
	rotation = 30

	#FIRST SCRIPT -> FOR JAVA PLAYER
	file_names = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith("log") and f.startswith("MPD")]
	print(file_names)
	
	#'delta_quality' additional info calculated from previous data
	format0 = ['capacity', 'action', 'quality', 'buf', 'rebuffering_time', 'reward', 'state1', 'state2', 'state3', 'state4', 'state5', 'state6', 'state7', 'state8', 'delta_quality']

	quality = []
	delta_quality = []
	rebuffering_time = []
	labels = []

	#testing
	capacity = []

	for file_name in file_names:
		print(file_name)
		f = open(os.path.join(path,file_name), 'r')

		payload = {}
		payload_values = {}

		samples = []
		i = 0 # samples
		j = 0 # algorithm
		rebuffering_count = 0 # count for rebuffering
		prev_quality = 0
		for line in f:
			j = j + 1
			if j == 2:
				algorithm = line[6:]
				print(algorithm)
				labels.append(algorithm)
			if line.startswith("INFO: {"):
				i = i + 1
				samples.append(i)
				
				param = line.split(',')
				pattern = r'[-+]?\d*\.\d+|\d+'

				for k in range(0,len(format0)-1):
					#print(format0[k])
					payload[format0[k]] = float(re.findall(pattern, param[k])[0])
					if payload_values.get(format0[k]) == None:
						payload_values[format0[k]] = []
					payload_values[format0[k]].append(payload[format0[k]])

				#print(payload)

				#calcolo delta
				if i == 1:
					prev_quality = payload['quality']
				if payload_values.get('delta_quality') == None:
						payload_values['delta_quality'] = []	
				payload_values['delta_quality'].append(payload['quality'] - prev_quality)
				prev_quality = payload['quality']

				#calcolo numero di eventi rebuffering
				if payload['rebuffering_time'] != 0:
					rebuffering_count = rebuffering_count + 1

		#plotto sulla stessa figura per ogni file (algoritmo) nella cartella i selezionata
		#salvo la figura per ogni algoritmo -> non va bene
	#1) reward nel tempo
		plt.figure(1)
		plt.plot(samples, payload_values['reward'], label = algorithm)
		lgd = plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.36), ncol=3)
		plt.xlabel('Video samples', fontsize=labelsize)
		plt.ylabel('Rewards', fontsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'rewards.png', bbox_inches='tight', bbox_extra_artists=(lgd,))
	#1) buffer nel tempo
		plt.figure(2)
		plt.plot(samples, payload_values['rebuffering_time'], label = algorithm)
		lgd = plt.legend(loc='lower center', bbox_to_anchor=(0.5,-0.36), ncol=3)
		plt.xlabel('Video samples', fontsize=labelsize)
		plt.ylabel('Rebuffering time', fontsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'rebuffering_time.png', bbox_inches='tight', bbox_extra_artists=(lgd,))
	#2) PDF o CDF della qualita e delle variazioni di qualita
		plt.figure(3)
		plt.plot(samples, payload_values['quality'], label = algorithm)
		lgd = plt.legend(loc='lower center', bbox_to_anchor=(0.5,-0.36), ncol=3)
		plt.xlabel('Video samples', fontsize=labelsize)
		plt.ylabel('Quality', fontsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'quality.png', bbox_inches='tight', bbox_extra_artists=(lgd,))

		plt.figure(4)
		plt.plot(samples, payload_values['delta_quality'], label = algorithm)
		lgd = plt.legend(loc='lower center', bbox_to_anchor=(0.5,-0.36), ncol=3)
		plt.xlabel('Video samples', fontsize=labelsize)
		plt.ylabel('Delta quality', fontsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'delta.png', bbox_inches='tight', bbox_extra_artists=(lgd,))

		# plt.figure(5)
		# plt.plot(samples, payload_values['capacity'], label = algorithm)
		# lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
		# plt.xlabel('Video samples')
		# plt.ylabel('Capacity')
		# if savefigs == True:
		# 	plt.savefig(path+'capacity.png', bbox_inches='tight', bbox_extra_artists=(lgd,))

		#data for boxplots
		quality.append(payload_values['quality'])
		delta_quality.append(payload_values['delta_quality'])
		#print(rebuffering_count)
		rebuffering_time.append(payload_values['rebuffering_time'])
		capacity.append(payload_values['capacity'])

	if len(file_names)!=0:
		print('first file')
		#3) Boxplot di qualita
		fig3, ax3 = plt.subplots()
		ax3.boxplot(quality)
		plt.ylabel('Quality', fontsize=labelsize)
		plt.xticks([1, 2, 3, 4, 5, 6], labels, rotation=rotation)
		ax3.tick_params(labelsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'boxplot_quality.png', bbox_inches='tight')

		#4) Boxplot delle variazioni di qualita
		fig4, ax4 = plt.subplots()
		ax4.boxplot(delta_quality)
		plt.ylabel('Delta', fontsize=labelsize)
		plt.xticks([1, 2, 3, 4, 5, 6], labels, rotation=rotation)
		ax4.tick_params(labelsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'boxplot_delta.png', bbox_inches='tight')

		#5) Boxplot di freeze rate (eventi di rebuffering)
		fig5, ax5 = plt.subplots()
		ax5.boxplot(rebuffering_time)
		plt.ylabel('Freeze', fontsize=labelsize)	
		plt.xticks([1, 2, 3, 4, 5, 6], labels, rotation=rotation)
		ax5.tick_params(labelsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'boxplot_rebuffering_time.png', bbox_inches='tight')

		#6) Spyder plot di qualità, delta qualità, freeze rate. Manca fairness per multiuser (per multiuser, jain's index: https://en.wikipedia.org/wiki/Fairness_measure)
		if savespider == True:
			plot_spider(path, quality, delta_quality, rebuffering_time, labels)
	
		#For testing
		#7) Capacity boxplot
		fig7, ax7 = plt.subplots()
		ax7.boxplot(capacity)
		plt.ylabel('Capacity', fontsize=labelsize)	
		plt.xticks([1, 2, 3, 4, 5, 6], labels, rotation=rotation)
		ax7.tick_params(labelsize=labelsize)
		if savefigs == True:
			plt.savefig(path+'boxplot_capacity.png', bbox_inches='tight')

	#END OF FIRST SCRIPT








	##SECOND SCRIPT -> FOR JAVASCRIPT PLAYER: BOLA AND PENSIEVE

	file_names = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder,f)) and f.startswith("log")]
	print(file_names)

	format1 = ['time_stamp', 'bit_rate', 'buffer_size', 'rebuffer_time', 'video_chunk_size', 'download_time', 'reward']
	formatSimple = ['lastRequest', 'lastquality', 'lastChunkStartTime', 'buf', 'nextChunkSize1', 'nextChunkSize2', 'nextChunkSize3', 'nextChunkSize4', 'nextChunkSize5', 'nextChunkSize6', 'bandwidthEst', 'RebufferTime', 'lastChunkFinishTime', 'Type', 'lastChunkSize']
	formatRL = ['lastRequest', 'lastquality', 'lastChunkStartTime', 'buf', 'bufferAdjusted', 'nextChunkSize1', 'nextChunkSize2', 'nextChunkSize3', 'nextChunkSize4', 'nextChunkSize5', 'nextChunkSize6', 'bandwidthEst', 'RebufferTime', 'lastChunkFinishTime', 'lastChunkSize']

	quality = []
	delta_quality = []
	rebuffer_time = []
	bit_rate = []
	labels = []

	for file_name in file_names:
		print(file_name)
		f = open(os.path.join(subfolder,file_name), 'r')

		payload = {}
		payload_values = {}

		if file_name == "log_simple_server":
			format2 = formatSimple
		else:
			format2 = formatRL

		i = 1 #line counter

		for line in f:
			if line != '\n':
				param = line.split('\t')
				param2 = param[7].split(', ')
				pattern = r'[-+]?\d*\.\d+|\d+'

				for k in range(0,len(format1)):
					payload[format1[k]] = float(param[k])
				
				for k in range(0,len(param2)):
					try:
						content = re.findall(pattern, param2[k])[0]
						payload[format2[k]] = float(content)
					except:
						payload[format2[k]] = 'Bola'
										
				if i!=2 and i!=1 and payload['lastRequest'] == 0:
					#print(payload_values['lastRequest'])
					if payload_values.get('Type') != None:
						algorithm = 'Bola'
					else:
						algorithm = 'Pensieve'
					print(algorithm)
					
					##PLOT HERE
					samples = payload_values['lastRequest']
				#1) reward nel tempo
					plt.figure(1)
					plt.plot(samples, payload_values['reward'], label = algorithm)
					lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
					plt.xlabel('Video samples')
					plt.ylabel('Rewards')

					if savefigs == True:
						plt.savefig(path+'rewardsJS.png', bbox_inches='tight', bbox_extra_artists=(lgd,))

				#2) buffer nel tempo
					plt.figure(2)
					plt.plot(samples, payload_values['rebuffer_time'], label = algorithm)
					lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
					plt.xlabel('Video samples')
					plt.ylabel('Rebuffering Time')

					if savefigs == True:
						plt.savefig(path+'rebuffering_timeJS.png', bbox_inches='tight', bbox_extra_artists=(lgd,))
				#3) plot qualità
					# plt.figure(3)
					# plt.plot(samples, payload_values['lastquality'], label = algorithm)
					# lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
					# plt.xlabel('Video samples')
					# plt.ylabel('Quality')

				#4) bitrate
					plt.figure(7)
					plt.plot(samples, payload_values['bit_rate'], label = algorithm)
					lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
					plt.xlabel('Video samples')
					plt.ylabel('Bitrate')
					if savefigs == True:
						plt.savefig(path+'bit_rateJS.png', bbox_inches='tight', bbox_extra_artists=(lgd,))
					##END PLOT HERE

					#for boxplots
					quality.append(payload_values['lastquality'])
					rebuffer_time.append(payload_values['rebuffer_time'])
					bit_rate.append(payload_values['bit_rate'])
					labels.append(algorithm)

					payload_values = {}

				for k in range(0,len(format1)):
					if payload_values.get(format1[k]) == None:
						payload_values[format1[k]] = []
					payload_values[format1[k]].append(payload[format1[k]])
				
				for k in range(0,len(param2)):
					if payload_values.get(format2[k]) == None:
						payload_values[format2[k]] = []

					payload_values[format2[k]].append(payload[format2[k]])

				i = i + 1

	if len(file_names)!=0:
		#4) Boxplot bitrate
		fig4, ax4 = plt.subplots()
		ax4.boxplot(bit_rate)
		ax4.set_title('Bitrate')
		plt.xticks([1, 2, 3, 4, 5, 6], labels)
		ax4.tick_params(labelsize=9)
		if savefigs == True:
			plt.savefig(path+'bitrateJS.png')

		#5) Boxplot di freeze rate (eventi di rebuffering)
		fig5, ax5 = plt.subplots()
		ax5.boxplot(rebuffer_time)
		ax5.set_title('Boxplot eventi di rebuffering')	
		plt.xticks([1, 2, 3, 4, 5, 6], labels)
		ax5.tick_params(labelsize=9)
		if savefigs == True:
			plt.savefig(path+'boxplot_rebuffering_timeJS.png')

	#END OF SECOND SCRIPT

	#FOR BOTH SCRIPTS	
	if savefigs == False and savespider == False:
		plt.show()

def main():
	subfolders = [f for f in os.listdir('.') if os.path.isdir(f)]   
	# print(subfolders)

	for subfolder in subfolders:
		#print(os.listdir(subfolder))
		test_numbers = [u for u in os.listdir(subfolder) if os.path.isdir(os.path.join(subfolder, u))]
		#print(test_numbers)
		for test_number in test_numbers:
			print(os.path.join(subfolder, test_number))
			main_script(subfolder, test_number)
			for k in range(1,4):
				plt.figure(k).clf()

if __name__ == "__main__":
	main()