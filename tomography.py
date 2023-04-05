# Подключение всех необходимых библиотек
import math

import functions as fn
import diff_evolution as de
import transformation as tf
import chip as ch

Pi = math.pi

# Начало исполнения скрипта
if __name__ == '__main__':
	
	# Установка параметров дифференциальной эволюции
	tomog_params = {
		'strategy': 'best1bin',
		'maxiter': 2000,
		'tol': 1e-5,
		'atol': 1e-7,
		'popsize': 10,
		'mutation': 0.5,
		'recombination': 1.0,
		'education_size': 30,
	}
	
	chip = ch.Chip(1, 1e-6)
	
 # Преобразование|№ Кубит | Параметры | Границы параметров  | Изменяемость параметров
	chip.set('phase',	1, [0],			[[0, 2*Pi]]						)
	chip.set('lossy',	1, [0.75, 0.8],	[[0.5, 1], [0.5, 1]]			)
	chip.set('BMS',		1, [0.5],		[[0.4, 0.6]]					)
	chip.set('phase',	1, [0],			[[0, 2*Pi]]						)
	chip.set('phase',	1, [0],			[[0, 2*Pi]], 		unfixed=True)
	chip.set('lossy',	1, [0.8, 0.75],	[[0.5, 1], [0.5, 1]]			)
	chip.set('BMS',		1, [0.5],		[[0.4, 0.6]]					)
	
	# Обучение
	train_data = fn.generateData(chip, tomog_params['education_size'])	
	[result, time] = de.differentialEvolution(chip, train_data, tomog_params, display=False)
	
	# Загрузка результатов томографии в файл
	fn.pushToFile(chip, tomog_params, result, time)
	
	
	
	
	
