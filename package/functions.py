# Подключение общих модулей
import numpy as np
import scipy.stats as st

# Подключение пользовательских модулей
from . import chip as ch


# Функция получения относительной фазы на выходах чипа
def getRelativePhase(state: np.array) -> tuple:
	normState = state / np.sqrt( np.power(np.abs(state), 2) )
	stateShift = normState * np.conj(normState[0])
	statePhase = np.angle(stateShift, deg=False)

	return (statePhase, stateShift)

# Функция получения фаз между выходами, как в эксперименте
def getExperimentPhase(state: np.array) -> np.array:	
	
	return []

# Функиция для определения отклонения предсказанного чипа от экспериментального
def getDeviation(chip:ch.Chip, data:list):
	
	# Оценки квадратов отклонений по разным параметрам
	deviation_pr_2 = 0
	deviation_t_2 = 0
	deviation_t_rel = 0
	deviation_phi = 0

	for d in data:
		# Инициализация входного и выходного состояний из массива data
		in_state_data = d[0].copy()
		out_state_data = d[1].copy()
		out_phi_data = d[2].copy()
		chip.changeUnfixedParams(d[3].copy())
		
		# Инициализация входного и выходного состояний предсказанного чипа
		in_state_pred = in_state_data.copy()
		out_state_pred = []
		
		# Вычисление выходного состояния предсказанного чипа
		out_state_pred = chip.compute(in_state_pred)

		# Вычисление разности фаз между выходами
		out_phi_pred, out_stateShift_pred = getRelativePhase(out_state_pred)

		out_state_pred = np.absolute(out_state_pred)
		out_state_pred = np.power(out_state_pred, 2)
			
		in_state_pred = np.absolute(in_state_pred)
		in_state_pred = np.power(in_state_pred, 2)

		out_state_data2 = np.multiply(out_state_data, np.exp(np.multiply(1j, out_phi_data)))
		out_state_pred2 = np.multiply(out_state_pred, out_stateShift_pred)

		# Определение оценок отклонения
		deviation_pr_2 	+= np.power	( np.abs(np.subtract(out_state_pred2 / out_state_pred.sum(), out_state_data2 / out_state_data.sum()) ), 2).sum()
		deviation_t_2 	+= np.power	(np.subtract(np.abs(out_state_pred), np.abs(out_state_data)) / in_state_pred.sum(), 2).sum()
  
		deviation_t_rel += np.abs	(out_state_pred).sum() / np.abs(out_state_data).sum()
		deviation_phi 	+= np.power	(np.subtract(out_phi_data, out_phi_pred), 2).sum()
 
 
	# Вычисление полного отклонения
	deviation = np.sqrt(deviation_pr_2 + deviation_t_2)

	return [deviation, np.sqrt(np.abs(deviation_pr_2)), np.sqrt(deviation_t_2), deviation_t_rel, np.sqrt(deviation_phi)] 
	

# Функиция для определения отклонения предсказанного чипа от экспериментального
def getTrainDeviation(chip	: ch.OpticalChip,
                      data	: list				) -> float:
	
	# Оценки квадратов отклонений по разным параметрам
	deviation_pr_2 = 0
	deviation_t_2 = 0
 
	for d in data:
		# Инициализация входного и выходного состояний из массива data
		inState 		= d[0].copy()
		outStateData 	= d[1].copy()
		outPhaseData 	= d[2].copy()
  
		chip.changeUnfixedArgs(d[3].copy())
		
		# Вычисление выходного состояния предсказанного чипа
		# matrix  = chip.getChipTransformation()
		# outStatePred = np.dot(matrix, inState)
		outStatePred = chip.compute(inState)

		# Вычисление разности фаз между выходами
		outPhasePred, out_stateShift_pred = getRelativePhase(outStatePred)

		outStatePredAbs = np.power(np.absolute(outStatePred), 2)
		inStateAbs 		= np.power(np.absolute(inState), 2)

		outStateData2 = np.multiply(outStateData, np.exp(np.multiply(1j, outPhaseData)))
		outStatePred2 = np.multiply(outStatePredAbs, out_stateShift_pred)

		# Определение оценок отклонения
		deviation_pr_2 	+= np.power	(np.abs( np.subtract(outStatePred2 / outStatePredAbs.sum(), outStateData2 / outStateData.sum()) ), 2).sum()
		deviation_t_2 	+= np.power	(np.subtract(np.abs(outStatePredAbs), np.abs(outStateData)) / inStateAbs.sum(), 2).sum()
 
	# Вычисление полного отклонения
	deviation = np.sqrt(deviation_pr_2 + deviation_t_2)

	return deviation 


# Функция генерации данных для обучения и тестирования
def generateData(chip: ch.Chip, size: int, regime: str, noise:float=0):
	# # data_vol - Объём информационной выборки для обучения и тестрирования
	#
	# # regime - режим входного состояния
	# 'f' = 'first'				- Входное состояние подаётся только в первый вход
	# 'aa' = 'alternately all'	- Входное состояние подаётся во все входы поочерёдно (за эксперимент)
	# 'ra' = 'random all'		- Входное состояние подаётся в произвольный вход по равномерному распрелделению
	# 'n' = 'normal'			- Входное состояние произвольное распределённое по нормальному распределению

	# Вся информация обучающей выборки
	data = list()

	# Инициализация входного и выходного состояний
	in_state = []
	out_state = []

	# Кол-во входов и выходов чипа
	num_inlet = int(np.power(2, chip.dimension))

	for i in range(size):
		# Присвоение значения входному состоянию, в
		# соответствие с режимом (regime)
		if		regime == 'f':
			in_state = np.eye(num_inlet)[:,[0]]

		elif	regime == 'aa':
			in_state = np.eye(num_inlet)

		elif	regime == 'ra':
			rn = np.random.random_integers(0, num_inlet-1, 1)
			in_state = np.eye(num_inlet)[:,[*rn]]

		elif	regime == 'n':
			in_state = np.random.normal(0, 1, [num_inlet, 1]) + 1j*np.random.normal(0, 1, [num_inlet, 1])
			in_state = in_state / np.sqrt( np.power(np.abs(in_state), 2).sum() )

		elif	regime == 's':
			alp = float(np.random.uniform(0, 2*np.pi, 1))
			in_state = np.array([[1], [np.exp(1j*alp)]], dtype=complex)

		else:
			raise ValueError(
				"ERROR::FUNCTION::GENERATE_DATA " + 
				"Функции передан неизвестный режим: regime = '" +
				regime + "'"
			)

		# Кол-во измерений на один эксперимент
		N = in_state.shape[1]
		
		for n in range(N):
			# Инициализация массивов
			unfixed_params = list()

			# Назначение изменяемых параметров чипа произвольными значениями
			for j in chip.unfixed_transforms:
				# Взятие информации о преобразование чипа
				transform = chip.transformations[j]
				num_of_params = transform.transform_info['num_args']
				params_bounds = transform.bounds
				
				# Заполнение массива изменяемых параметров
				for k in range(num_of_params):
					bounds = params_bounds[k]
					unfixed_params.append(*np.random.uniform(bounds[0], bounds[1], 1))

			chip.changeUnfixedParams(unfixed_params)
			out_state = chip.compute(in_state[:,[n]])

			# Вычисление разности фаз между выходами
			phi_out_state, out_stateShift = getRelativePhase(out_state)

			out_state = np.abs(out_state)
			out_state = np.power(out_state, 2)

			if noise != 0:
				mistake = np.abs(np.random.normal(0, noise, [in_state.shape[0], 1]))
				out_state += out_state*mistake
		
			data.append(tuple([in_state[:,[n]], out_state, phi_out_state, unfixed_params])) # 

	return data

# Функция генерации данных для обучения и тестирования
def generateData2(chip	: ch.OpticalChip,
                  size	: int,
                  regime: str	= 'n',
                  noise	: float = 0):
	# # data_vol - Объём информационной выборки для обучения и тестрирования
	#
	# # regime - режим входного состояния
	# 'f' = 'first'				- Входное состояние подаётся только в первый вход
	# 'aa' = 'alternately all'	- Входное состояние подаётся во все входы поочерёдно (за эксперимент)
	# 'ra' = 'random all'		- Входное состояние подаётся в произвольный вход по равномерному распрелделению
	# 'n' = 'normal'			- Входное состояние произвольное распределённое по нормальному распределению

	# Вся информация обучающей выборки
	data = list()

	# Инициализация входного и выходного состояний
	inState		: np.array	= []
	outState 	: np.array	= []

	# Кол-во входов и выходов чипа
	chipSize = chip._chipSize

	for i in range(size):
		# Присвоение значения входному состоянию, в
		# соответствие с режимом (regime)
		if		regime == 'f':
			inState = np.eye(chipSize)[:,[0]]

		elif	regime == 'aa':
			inState = np.eye(chipSize)

		elif	regime == 'ra':
			rn = np.random.random_integers(0, chipSize-1, 1)
			inState = np.eye(chipSize)[:,[*rn]]

		elif	regime == 'n':
			inState = np.random.normal(0, 1, [chipSize, 1]) + 1j*np.random.normal(0, 1, [chipSize, 1])
			inState = inState / np.sqrt( np.power(np.abs(inState), 2).sum() )

		elif	regime == 's':
			alp = float(np.random.uniform(0, 2*np.pi, 1))
			inState = np.array([[1], [np.exp(1j*alp)]], dtype=complex)

		else:
			raise ValueError(
				"ERROR in generateData with parameter 'regime'. " + 
				f"Функции передан неизвестный режим: '{regime}'!"
			)

		# Кол-во измерений на один эксперимент
		N = inState.shape[1]
		
		for i in range(N):
			# Инициализация массивов
			unfixedArgs = list()

			# Назначение изменяемых параметров чипа произвольными значениями
			for j in chip._unfixedTransformations:
				# Взятие информации о преобразование чипа
				transformation = chip._transformations[j]
				argsNum = transformation._argsNum
				bounds = transformation._bounds
				
				# Заполнение массива изменяемых параметров
				for k in range(argsNum):
					bound = bounds[k]
					unfixedArgs.append(*np.random.uniform(bound[0], bound[1], 1))

			chip.changeUnfixedArgs(unfixedArgs)
			outState = np.dot(chip.getChipTransformation(), inState[:,[i]])

			# Вычисление разности фаз между выходами
			phi_outState, outStateShift = getRelativePhase(outState)

			outState = np.power(np.abs(outState), 2)

			if noise != 0:
				mistake = np.abs(np.random.normal(0, noise, [inState.shape[0], 1]))
				outState += outState * mistake
		
			data.append(tuple([inState[:,[i]], outState, phi_outState, unfixedArgs])) # 

	return data


def testingDeviation(chip: ch.Chip, test_data: list, pred_params: list):
	
	tchip = chip.copy()
	tchip.changeFixedParams(pred_params)
	
	deviate = list()
	deviate_pr = list()
	deviate_t = list()
	deviate_t_rel = list()
	deviate_phi = list()
		
	for data in test_data:
		deviations = getDeviation(tchip, [data])
	
		deviate.append(deviations[0])
		deviate_pr.append(deviations[1])
		deviate_t.append(deviations[2])
		deviate_t_rel.append(deviations[3])
		deviate_phi.append(deviations[4])

	return [deviate, deviate_pr, deviate_t, deviate_t_rel, deviate_phi]



def calTestInfo(deviations: list):

	info = dict()

	info['M[p]']		= np.mean(deviations[0])
	info['M[pPr]']		= np.mean(deviations[1])
	info['M[pT]']		= np.mean(deviations[2])
	info['M[pTrel]']	= np.mean(deviations[3])
	info['M[pPhi]']		= np.mean(deviations[4])

	info['D[p]']		= np.var(deviations[0])
	info['D[pPr]'] 		= np.var(deviations[1])
	info['D[pT]'] 		= np.var(deviations[2])
	info['D[pTrel]'] 	= np.var(deviations[3])
	info['D[pPhi]'] 	= np.var(deviations[4])

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
	info['pPhi_max']	= np.max(deviations[4])

	info['p_min']		= np.min(deviations[0])
	info['pPr_min']		= np.min(deviations[1])
	info['pT_min']		= np.min(deviations[2])
	info['pTrel_min']	= np.min(deviations[3])
	info['pPhi_min']	= np.min(deviations[4])

	return info

	

def chipFromInfo(info: dict):

	result_x		= info['charac_result']['result.x']
	chip_dim		= info['chip_info']['dimention']
	transformations	= info['chip_info']['transforms']
	
	chip = ch.Chip(chip_dim)
	
	for i in range(len(transformations)):

		transform	= transformations[i]

		if transform['name'] == "phaseb":
			name	= "phase"
		else:
			name	= transform['name']
		inlet		= transform['inlet']
		parameters	= transform['parameters']
		bounds		= transform['bounds']
		unfixed		= transform['unfixed']

		chip.set(name, inlet, parameters, bounds, unfixed=unfixed)

	return [chip, result_x]



