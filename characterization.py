# Подключение общих модулей
from math import pi
import sys

# Подключение пользовательских модулей
# из папки package
import package.chip as ch
import package.functions as fn
import package.data_files as df
import package.diff_evolution as de



# Начало исполнения скрипта характеризации
if __name__ == '__main__':
	
	# Считывание пути к формируемой директории в папке ./result
	dir_pass = sys.argv[1]
	# Считывание или установка уровня шума при детектирование
	if len(sys.argv) >= 3:
		noise = float(sys.argv[2])
	else:
		noise = 1e-6

	# Установка параметров томографии
	charac_params = {
		'strategy': 'best1bin',
		'maxiter': 500,
		'tol': 1e-5,
		'popsize': 30,
		'mutation': 0.7,
		'recombination': 1.0,
		'education_volume': 10,
		'noise': noise,
		'regime': 'aa'
	}
	
	chip = ch.Chip(1)
	
 # Преобразование| № Канала | Параметры | Границы параметров | Изменяемость параметров
	chip.set('phase',	1, [0],			[[0, 2*pi]]					)
	chip.set('lossy',	1, [0.75, 0.8],	[[0.5, 1], [0.5, 1]]		)
	chip.set('bms',		1, [0.5],		[[0.4, 0.6]]				)
	chip.set('phase',	1, [0],			[[0, 2*pi]]					)
	chip.set('phase',	1, [0],			[[0, 2*pi]],	unfixed=True)
	chip.set('lossy',	1, [0.8, 0.75],	[[0.5, 1], [0.5, 1]]		)
	chip.set('bms',		1, [0.5],		[[0.4, 0.6]]				)

	# Генерация обучающей выборки
	train_data = fn.generateData(
		chip,
		charac_params['education_volume'],
		regime=charac_params['regime'],
		noise=charac_params['noise']
	)

	# Метод дифференциальной эволюции
	[result, time, attempt] = de.differentialEvolution(
		chip,
		train_data,
		charac_params,
		display=True
	)

	# Создаём словарь со всеми данными характеризации
	info: dict = {
		'chip_info': chip.getChipSetupInfo(),
		'charac_params': charac_params,
		'charac_result': {
			'attemps': attempt,
			'time': time,
			'nit': result.nit,
			'result.x': result.x,
			'result.fun': result.fun
		}
	}

	# Загрузка результатов характериазции в файл
	df.pushToDataFile(info, dir_pass, gendir=True)
	
	
	
	
	
