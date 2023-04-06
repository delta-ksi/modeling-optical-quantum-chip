# Подключение общих модулей
import numpy as np
import scipy.stats as st
import pickle
import datetime

# Подключение пользовательских модулей
from . import chip as ch



# Функиция для определения отклонения предсказанного чипа от экспериментального
def getDeviation(chip, data):
	
	# Оценки квадратов отклонений по разным параметрам
	deviation_pr_2 = 0
	deviation_t_2 = 0
	deviation_t_rel = 0

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
		deviation_t_rel = out_state_pred.sum() / out_state_data.sum()
		
	# Вычисление полного отклонения
	deviation = np.sqrt(deviation_pr_2 + 5*deviation_t_2)
	
	return [deviation, np.sqrt(deviation_pr_2), np.sqrt(deviation_t_2), deviation_t_rel]
	


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
	


def testingDeviation(chip, test_data, pred_params):
	
	tchip = chip.copy()
	tchip.changeFixedParams(pred_params)
	
	deviate = list()
	deviate_pr = list()
	deviate_t = list()
	deviate_t_rel = list()
		
	for data in test_data:			
		
		deviations = getDeviation(tchip, [data])
	
		deviate.append(deviations[0])
		deviate_pr.append(deviations[1])
		deviate_t.append(deviations[2])
		deviate_t_rel.append(deviations[3])

	return [deviate, deviate_pr, deviate_t, deviate_t_rel]



def calTestInfo(deviations):
	
	info = dict()

	info['M[p]']		= np.mean(deviations[0])
	info['M[pPr]']		= np.mean(deviations[1])
	info['M[pT]']		= np.mean(deviations[2])
	info['M[pTrel]']	= np.mean(deviations[3])

	info['D[p]']		= np.var(deviations[0])
	info['D[pPr]'] 		= np.var(deviations[1])
	info['D[pT]'] 		= np.var(deviations[2])
	info['D[pTrel]'] 	= np.var(deviations[3])

	info['Q_0.9[p]']	= np.quantile(deviations[0], 0.9)
	info['Q_0.9[pPr]'] 	= np.quantile(deviations[1], 0.9)
	info['Q_0.9[pT]'] 	= np.quantile(deviations[2], 0.9)

	info['P_0.9']		= st.t.interval(
								0.9,
								len(deviations[3])-1,
								loc=np.mean(deviations[3]),
								scale=st.sem(deviations[3])
							)

	info['p_max']		= np.max(deviations[0])
	info['pPr_max']		= np.max(deviations[1])
	info['pT_max']		= np.max(deviations[2])
	info['pTrel_max']	= np.max(deviations[3])

	return info



def pushToFile(data, file_pass="", gen=True):

	if gen:
		# Генерирование файла
		today = datetime.datetime.today()
		file_pass = './data/' + today.strftime('%Y-%m-%d_%H:%M:%S') + '.dat'
	
	# Запись всех данных томографии в файл
	with open(file_pass, 'wb') as f:
		pickle.dump(data, f)



def pullFromFile(file_pass):

	# Чтение всех данных моделирования из файла
	data = dict()
	with open(file_pass, 'rb')	as f:
		data = pickle.load(f)
	
	return data


def chipFromInfo(info):

	result_x		= info['model_result']['result.x']
	chip_dim		= info['chip_info']['dimention']
	transformations	= info['chip_info']['transforms']
	noise			= info['chip_info']['noise']
	
	chip = ch.Chip(chip_dim, noise)
	
	for i in range(len(transformations)):

		transform	= transformations[i]

		name		= transform['name']
		inlet		= transform['inlet']
		parameters	= transform['parameters']
		bounds		= transform['bounds']
		unfixed		= transform['unfixed']

		chip.set(name, inlet, parameters, bounds, unfixed=unfixed)

	return [chip, result_x]



