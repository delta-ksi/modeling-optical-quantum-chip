# Подключение общих модулей
from math import pi

# Подключение пользовательских модулей
# из папки package
import package.chip as ch
import package.functions as fn
import package.diff_evolution as de



# Начало исполнения скрипта
if __name__ == '__main__':
	
	# Установка параметров томографии
	tomog_params = {
		'strategy': 'best1bin',
		'maxiter': 10,
		'tol': 1e-5,
		'atol': 1e-7,
		'popsize': 10,
		'mutation': 0.5,
		'recombination': 1.0,
		'education_volume': 30
	}
	
	chip = ch.Chip(1, 1e-6)
	
 # Преобразование| № Кубит | Параметры | Границы параметров  | Изменяемость параметров
	chip.set('phase',	1, [0],			[[0, 2*pi]]					)
	chip.set('lossy',	1, [0.75, 0.8],	[[0.5, 1], [0.5, 1]]		)
	chip.set('BMS',		1, [0.5],		[[0.4, 0.6]]				)
	chip.set('phase',	1, [0],			[[0, 2*pi]]					)
	chip.set('phase',	1, [0],			[[0, 2*pi]],	unfixed=True)
	chip.set('lossy',	1, [0.8, 0.75],	[[0.5, 1], [0.5, 1]]		)
	chip.set('BMS',		1, [0.5],		[[0.4, 0.6]]				)
	
	# Обучение
	train_data = fn.generateData(chip, tomog_params['education_size'])	
	[result, time] = de.differentialEvolution(chip, train_data, tomog_params, display=False)
	
	# Создаём словарь со всеми данными томографирования
	info = {
		'chip_info': chip.getChipSetupInfo(),
		'tomog_params': tomog_params,
		'tomog_result': {
			'time': time,
			'nit': result.nit,
			'result.x': result.x,
			'result.fun': result.fun
		}
	}

	# Загрузка результатов томографии в файл
	fn.pushDataToFile(info, gen=True)
	
	
	
	
	
