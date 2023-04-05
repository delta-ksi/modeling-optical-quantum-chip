# Подключение всех необходимых библиотек

import numpy as np
import pickle
import datetime as dt_tm

# Функиция для определения отклонения предсказанного чипа от экспериментального
def getDeviation(chip, data):
	
	# Оценки квадратов отклонений по разным параметрам
	deviation_pr_2 = 0
	deviation_t_2 = 0
	
	for d in data:
		# Инициализация входного и выходного состояний из массива data
		in_state_data = d[0]
		out_state_data = d[1]
		chip.changeUnfixedParams(d[2])
		
		# Инициализация входного и выходного состояний предсказанного чипа
		in_state_pred = in_state_data.copy()
		out_state_pred = []
		
		# Вычисление выходного состояния предсказанного чипа
		out_state_pred = chip.compute(in_state_pred)
		out_state_pred = np.absolute(out_state_pred)
		out_state_pred = np.power(out_state_pred, 2)
			
		in_state_pred = np.absolute(in_state_pred)
		in_state_pred = np.power(in_state_pred, 2)
			
		# Определение оценок отклонения
		deviation_pr_2 += np.power(np.subtract(out_state_pred / out_state_pred.sum(), out_state_data / out_state_data.sum()), 2).sum()
		deviation_t_2 += np.power(np.subtract(out_state_pred, out_state_data) / in_state_pred.sum(), 2).sum()
		
	# Вычисление полного отклонения
	deviation = np.sqrt(deviation_pr_2 + 5*deviation_t_2)
	
	return [deviation, np.sqrt(deviation_pr_2), np.sqrt(deviation_t_2)]
	
# Функция генерации данных для обучения и тестирования
def generateData(chip, data_vol, input_norm_dis=False, return_unnoise_too=False):
	
	# Инициализация входного и выходного состояния
	# @ Необходимо расширять вектор для n размерности чипа
	in_state = np.array([[1], [0]])
	out_state = []
	
	# Вся информация обучающей выборки
	data = list()
	if return_unnoise_too:
		data_unnoise = list()

	for i in range(data_vol):
		unfixed_params = list()
		
		if input_norm_dis == True:
			in_state = np.random.normal(0, 1, [2, 1]) + 1j*np.random.normal(0, 1, [2, 1])
			in_state = in_state / np.sqrt( np.power(np.abs(in_state), 2).sum() )
		
		for j in chip.unfixed_transforms:
			num_of_params = chip.transformations[j].transform_info['num_args']

			params_bounds = chip.transformations[j].bounds
			
			for k in range(num_of_params):
				bounds = params_bounds[k]
				unfixed_params.append(*np.random.uniform(bounds[0], bounds[1], 1))
		
		chip.changeUnfixedParams(unfixed_params)

		out_state_unnoise = []
		if return_unnoise_too:
			[out_state, out_state_unnoise] = chip.compute(in_state, return_unnoise_too)

			out_state = np.absolute(out_state)
			out_state = np.power(out_state, 2)

			out_state_unnoise = np.absolute(out_state_unnoise)
			out_state_unnoise = np.power(out_state_unnoise, 2)

			data.append(tuple([in_state, out_state, unfixed_params]))
			data_unnoise.append(tuple([in_state, out_state_unnoise, unfixed_params]))
		else:
			out_state = chip.compute(in_state)

			out_state = np.absolute(out_state)
			out_state = np.power(out_state, 2)
		
			data.append(tuple([in_state, out_state, unfixed_params]))

	return data
	
def pushToFile(chip, dif_evo_params, result, time):
	# Генерирование файла
	today = dt_tm.datetime.today()
	file_pass = './data/' + today.strftime('%Y-%m-%d_%H:%M:%S') + '.dat'

	# Создаём словарь со всеми данными томографирования
	data = {
		'chip_info': chip.getChipSetupInfo(),
		'dif_evo_params': dif_evo_params,
		'model_result': {
			'time': time,
			'nit': result.nit,
			'result.x': result.x,
			'result.fun': result.fun
		}
	}
	
	# Запись всех данных томографии в файл
	with open(file_pass, 'wb') as f:
		pickle.dump(data, f)





