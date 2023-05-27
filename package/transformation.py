# Подключение общих модулей
import math as m
import numpy as np
import cmath as cm



# Функции возвращающие матрицы преобразования гейтов

# Фазовая задержка
def tPhase(arguments):
	phase = arguments[0]
	
	u = np.array(
		[[1, 	0		],
		 [0, 	cm.exp(1j*phase)]],
		dtype=complex
	)
	
	return u

# Потери в каналах
def tLossy(arguments):
	t0 = arguments[0]
	t1 = arguments[1]
	
	u = np.array(
		[[m.sqrt(t0), 0			],
		 [0,		 m.sqrt(t1)	]],
		dtype=complex
	)
	
	return u

# Не поляр. светоделитель
def tBMS(arguments):
	r = arguments[0]

	u = np.array(
		[[m.sqrt(r),  -m.sqrt(1-r) ],
		 [m.sqrt(1-r), m.sqrt(r)   ]],
		dtype=complex
	)

	return u

# Словарь, хранящий всю информацию о
# квантовых преобразованиях
transformations_list = {
	'phase': {
		'num_args': 1,
		'pointer': tPhase 
	},
	'lossy': {
		'num_args': 2,
		'pointer': tLossy
	},
	'bms': {
		'num_args': 1,
		'pointer': tBMS
	}
}

# Общий класс всех гейтов оптического чипа реализующий их преобразование
class Transformation:
	def set(self, arguments):
		self.transform = np.kron(np.kron(
			np.eye(int(m.pow(2, self.inlet - 1))),
			self.transform_matrix_func(arguments)),
			np.eye(int(m.pow(2, self.chip_dimension - self.inlet)))
		)

	def __init__(self, tid, name_tran_mat_fun, chip_params, transform_params, bounds):
		# сhip_parameters
		# [0] Размерность чипа (с каким кол-ом кубитов он работает)
		# [1] На какой кубит(ы) действует преобразование
		
		self.id = tid # transformation id
		
		# Обработка ошибки неверно указанного преобразования
		if transformations_list.get(name_tran_mat_fun) != None:
			self.transform_info = transformations_list[name_tran_mat_fun].copy()
			self.transform_info.pop('pointer')
		else:
			raise ValueError(
				'CLASS::TRANSFORMATION::INIT' + 
				'Неизвестное квантовое преобразование: ' +
				name_tran_mat_fun
			)
		
		self.chip_dimension = chip_params[0]
		self.inlet = chip_params[1]
		
		self.transform_info['name'] = name_tran_mat_fun
		self.transform_info['inlet'] = self.inlet
		self.transform_info['parameters'] = transform_params
		self.transform_info['bounds'] = bounds
		
		self.transform_matrix_func = transformations_list[name_tran_mat_fun]['pointer']
		
		# Обработка ошибки неверного указания количества аргументов преобразования
		if len(transform_params) != self.transform_info['num_args']:
			raise ValueError(
				'CLASS::TRANSFORMATION::INIT ' + 
				'Передано неверное количество аргументов преобразования ' +
				name_tran_mat_fun + ' ' + 
				len(transform_params) + ' вместо ' +
				self.transform_info['num_args']
			)
		
		self.bounds = bounds

		self.set(transform_params)
		
	def __call__(self, vector):
		return np.dot(self.transform, vector)
	
	
	
	
	
