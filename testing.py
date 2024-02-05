# Подключение общих модулей
import sys

# Подключение пользовательских модулей
# из папки package
import package.data_files as df
import package.functions as fn
import package.plot as plt
import package.chip as ch


import numpy as np
# Начало исполнения скрипта тестирования
if __name__ == '__main__':
	
	parameters = {
		'test-volume'	: int(1e4),
		'regime'		: 'n'
	}

	# Считывание путей к .dat файлам из аргументов, который будет тестироваться
	dirsPass = sys.argv[1:]
	num = len(dirsPass)
 
	deviations : dict = {
		'D'		: list(),
		'Pr'	: list(),
		'T'		: list(),
		'Trel'	: list(),
		'Phase'	: list()
	}

	info = dict()
	for i, dp in enumerate(dirsPass):
		print("Testing " + str(i) + ": " + str(dp))

		# Взятие словаря info из файла и взятие из него необходимых параметров
		chipInfo 				: dict				= df.pullFromDataFile(dp, 'chip-info')
		characterizationInfo 	: dict				= df.pullFromDataFile(dp, 'characterization-result')
		chip 					: ch.OpticalChip 	= ch.chipFromInfo(chipInfo)
		predictedArgs 			: list 				= fn.predictedArgsFromInfo(characterizationInfo)

		# Тестирование
		testData = fn.generateData2(
      		chip,
        	size 	= parameters['test-volume'],
         	regime 	= parameters['regime']
        )
		__deviations = fn.testingDeviation(chip, testData, predictedArgs)

		statisticalInfo = fn.computeStatisticalInfo(__deviations)
		info['parameters'] 			= parameters
		info['statistical-info'] 	= statisticalInfo
  
		df.pushToDataFile(
			info,
			dp,
			fileName = 'testing-result'
		)
		df.pushToTextFile(
			info,
			dp + '/info',
			fileName = 'testing-result'
		)
		
		for key in [*deviations]:
			# __deviations[key] = -(__deviations[key] - characterizationInfo['parameters']['noise'])
			deviations[key] = [*deviations[key], *__deviations[key]]
	
	statisticalInfo = fn.computeStatisticalInfo(deviations)
	
	if num == 1:
		plt.plotHists(deviations, statisticalInfo, dirsPass[0] + "/plot")
	else:
		plt.plotHists(deviations, statisticalInfo, "./")
	
	
	
