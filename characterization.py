# Подключение общих модулей
from math import pi
import sys

# Подключение пользовательских модулей
# из папки package
import package.chip as ch
import package.transformation as tf
import package.functions as fn
import package.data_files as df
import package.diff_evolution as de

import numpy as np

# Начало исполнения скрипта характеризации
if __name__ == '__main__':
	# '''
	# Считывание пути к формируемой директории в папке ./result
	dirPass = sys.argv[1]
	# Считывание или установка уровня шума при детектирование
	if len(sys.argv) >= 3:
		noise = float(sys.argv[2])
	else:
		noise = 1e-2

	# Установка параметров характеризации
	# charac_params = {
	# 	'strategy': 			'best1bin',
	# 	'maxiter': 				10000,
	# 	'tol': 					1e-5,
	# 	'popsize': 				30,
	# 	'mutation': 			0.7,
	# 	'recombination': 		1.0,
	# 	'education_volume': 	1,
	# 	'noise':		 		noise,
	# 	'regime': 				'n'
	# }

	# chip = ch.Chip(2)
 # Преобразование| № Канала | Параметры | Границы параметров | Изменяемость параметров
	# chip.set('phase',	1, 		[],		[[0, 2*pi]]							)
	# chip.set('phase',	1, 		[],		[[0, 2*pi]],			unfixed=True)
	# chip.set('lossy',	1, 		[],		[[0.5, 1], [0.5, 1]]				)
	# chip.set('bms',		1, 		[],		[[0.4, 0.6]]						)
	# chip.set('phase',	1, 		[],		[[0, 10*pi]]						)
	# chip.set('phase',	1, 		[],		[[0, 2*pi]],			unfixed=True)
	# chip.set('lossy',	1, 		[],		[[0.5, 1], [timer = time.perf_counter()			unfixed=True)
	# chip.set('lossy',	1, 		[],		[[0.5, 1], [0.5, 1]]				)

	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]]				)
	# chip.set('2lossy',	1, 		[],		[[0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1]]		)
	# chip.set('2bms',	1, 		[],		[[0.4, 0.6], [0.4, 0.6]]						)
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]], 	unfixed=True) # [[0, 2*pi], [0, 2*pi], [0, 2*pi]]
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]]				)
	# chip.set('2lossy',	1, 		[],		[[0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1]]		)
	# chip.set('2bms',	1, 		[],		[[0.4, 0.6], [0.4, 0.6]]						)
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]], 	unfixed=True)
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]]				)
	# chip.set('2lossy',	1, 		[],		[[0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1]]		)
	# chip.set('1bms2',	1, 		[],		[[0.4, 0.6]]									)
	# chip.set('1phase2',	1, 		[],		[[0, 2*pi], [0, 2*pi]]							)
	# chip.set('1lossy2',	1, 		[],		[[0.5, 1], [0.5, 1]]							)
	# chip.set('1bmsM',	1, 		[],		[[0.4, 0.6]]									)
	# chip.set('1phaseM',	1, 		[],		[[0, 2*pi], [0, 2*pi]]							)
	# chip.set('1lossyM',	1, 		[],		[[0.5, 1], [0.5, 1]]							)
	# chip.set('1bms2',	1, 		[],		[[0.4, 0.6]]									)
	# chip.set('1phase2',	1, 		[],		[[0, 2*pi], [0, 2*pi]]							)
	# chip.set('1lossy2',	1, 		[],		[[0.5, 1], [0.5, 1]]							)
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]], 	unfixed=True)
	# chip.set('2bms',	1, 		[],		[[0.4, 0.6], [0.4, 0.6]]						)
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]], 	unfixed=True)
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]]				)
	# chip.set('2lossy',	1, 		[],		[[0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1]]		)
	# chip.set('2bms',	1, 		[],		[[0.4, 0.6], [0.4, 0.6]]						)
	# chip.set('2phase',	1, 		[],		[[0, 2*pi], [0, 2*pi], [0, 2*pi]]				)
	# chip.set('2lossy',	1, 		[],		[[0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1]]		)

	# args = chip.getArgs()

	# # Генерация обучающей выборки
	# train_data = fn.generateData(
	# 	chip,
	# 	charac_params['education_volume'],
	# 	regime=charac_params['regime'],
	# 	noise=charac_params['noise']
	# )
	
	# print(len(train_data))

	# # Метод дифференциальной эволюции
	# [result, time, attempt] = de.differentialEvolution(
	# 	chip,
	# 	train_data,
	# 	charac_params,
	# 	display=True
	# )

	# # Создаём словарь со всеми данными характеризации
	# info: dict = {
	# 	'chip_info': chip.getChipSetupInfo(),
	# 	'charac_params': charac_params,
	# 	'charac_result': {
	# 		'attemps': attempt,
	# 		'time': time,
	# 		'nit': result.nit,
	# 		'result.x': result.x,
	# 		'result.fun': result.fun
	# 	}
	# }
	# # Загрузка результатов характериазции в файл
	# df.pushToDataFile(info, dirPass, gendir=True)
	# # '''
	
	# Установка параметров характеризации
	parameters = {
		'strategy': 			'best1bin',
		'maxiter': 				1200,
		'tol': 					1e-5,
		'popsize': 				30,
		'mutation': 			0.7,
		'recombination': 		1.0,
		'train-volume': 		50,
		'noise':		 		noise,
		'regime': 				'n'
	}
 
	Ochip = ch.get_CNOT_ODRS_chip()
	# Ochip.changeArgs(args)
 
	# inState = np.random.normal(0, 1, [4, 1]) + 1j*np.random.normal(0, 1, [4, 1])
	# inState = inState / np.sqrt( np.power(np.abs(inState), 2).sum() )
	# outState = chip.compute(inState)
	# # outState2 = matrix @ inState
	# outState2 = Ochip.compute(inState)
	# print(np.abs(outState2-outState).sum())
 
	# fixedArgsBounds = Ochip.getFixedArgsBounds()
 
	# args = list()
	# for bounds in fixedArgsBounds:
	# 	args.append(float(np.random.uniform(bounds[0], bounds[1], 1)))
 
	chipInfo	: dict 	= Ochip.getChipInfo()
	dataDirPass	: str	= df.createDataDir(dirPass)
	infoDirPass : str 	= df.createDataDir(dataDirPass, "info")

	df.pushToDataFile(
    	chipInfo,
     	dataDirPass,
      	fileName	= 'chip-info'
    )
	df.pushToTextFile(
     	chipInfo,
      	infoDirPass,
       	fileName	= 'chip-info'
    )
 
	# Генерация обучающей выборки
	trainData = fn.generateData2(
		Ochip,
		size	= parameters['train-volume'],
		regime	= parameters['regime'],
		noise	= parameters['noise']
	)
	
	# times = list()
	# for i in range(10000):
	# 	timer = time.perf_counter()
	# 	Ochip.changeFixedArgs(args)
	# 	fn.getTrainDeviation(Ochip, trainData)
	# 	times.append(time.perf_counter() - timer)
 
	# times2 = list()
	# for i in range(10000):
	# 	timer = time.perf_counter()
	# 	chip.changeFixedParams(args)
	# 	fn.getDeviation(chip, trainData)
	# 	times2.append(time.perf_counter() - timer)
  
	# print(np.mean(times) - np.mean(times2))
	# print(np.sqrt(np.var(times)) + np.sqrt(np.var(times2)))
 
	# deviations = fn.getDeviation(chip, trainData)
	# deviation = fn.getTrainDeviation(Ochip, trainData)
	
	# print(deviations[0])
	# print(deviation)
 
	# Метод дифференциальной эволюцииchipName
	result = de.differentialEvolution2(
		Ochip,
		data 	= trainData,
		params 	= parameters,
		display	= False
	)
 
	# Создаём словарь со всеми данными характеризации
	info : dict = {
		'chip-name'		: Ochip._name,
		'parameters'	: parameters,
		'result'		: result
	}
 
	# Загрузка результатов характериазции в файл
	df.pushToDataFile(
     	info,
      	dataDirPass,
       	fileName = 'characterization-result'
    )
	df.pushToTextFile(
     	info,
      	infoDirPass,
       	fileName = 'characterization-result'
    )
