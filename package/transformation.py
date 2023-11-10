# Подключение общих модулей
import math as m
import numpy as np
import cmath as cm
import copy



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

# 
def t2Phase(arguments):
	p0 = arguments[0]
	p1 = arguments[1]
	p2 = arguments[2]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, cm.exp(1j*p0), 0, 0],
		 [0, 0, cm.exp(1j*p1), 0],
		 [0, 0, 0, cm.exp(1j*p2)]],
		dtype=complex
	)
	
	return u

# 
def t2Lossy(arguments):
	t0 = arguments[0]
	t1 = arguments[1]
	t2 = arguments[2]
	t3 = arguments[3]
	
	u = np.array(
		[[m.sqrt(t0), 0, 0, 0],
		 [0, m.sqrt(t1), 0, 0],
		 [0, 0, m.sqrt(t2), 0],
		 [0, 0, 0, m.sqrt(t3)]],
		dtype=complex
	)
	
	return u

# 
def t2BMS(arguments):
	r0 = arguments[0]
	r1 = arguments[1]
	
	u = np.array(
		[[m.sqrt(r0), -m.sqrt(1-r0), 0, 0],
		 [m.sqrt(1-r0), m.sqrt(r0), 0, 0],
		 [0, 0, m.sqrt(r1), -m.sqrt(1-r1)],
		 [0, 0, m.sqrt(1-r1), m.sqrt(r1)]],
		dtype=complex
	)
	
	return u

# 
def t1BMS2(arguments):
	r = arguments[0]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, 1, 0, 0],
		 [0, 0, m.sqrt(r), -m.sqrt(1-r)],
		 [0, 0, m.sqrt(1-r), m.sqrt(r)]],
		dtype=complex
	)
	
	return u

# 
def t1Phase2(arguments):
	p0 = arguments[0]
	p1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, 1, 0, 0],
		 [0, 0, cm.exp(1j*p0), 0],
		 [0, 0, 0, cm.exp(1j*p1)]],
		dtype=complex
	)
	
	return u


# 
def t1Phase1(arguments):
	p0 = arguments[0]
	p1 = arguments[1]
	
	u = np.array(
		[[cm.exp(1j*p0), 0, 0, 0],
		 [0, cm.exp(1j*p1), 0, 0],
		 [0, 0, 1, 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u

# 
def t1Lossy2(arguments):
	t0 = arguments[0]
	t1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, 1, 0, 0],
		 [0, 0, m.sqrt(t0), 0],
		 [0, 0, 0, m.sqrt(t1)]],
		dtype=complex
	)
	
	return u

# 
def t1BMSM(arguments):
	r = arguments[0]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, m.sqrt(r), -m.sqrt(1-r), 0],
		 [0, m.sqrt(1-r), m.sqrt(r), 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u

# 
def t1PhaseM(arguments):
	p0 = arguments[0]
	p1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, cm.exp(1j*p0), 0, 0],
		 [0, 0, cm.exp(1j*p1), 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u

# 
def t1LossyM(arguments):
	t0 = arguments[0]
	t1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, m.sqrt(t0), 0, 0],
		 [0, 0, m.sqrt(t1), 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u

# Словарь, хранящий всю информацию о
# квантовых преобразованиях
transformations_list = {
    '1phase1': {
		'num_args': 2,
		'pointer': t1Phase1 
	},
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
	},
	'2phase': {
		'num_args': 3,
		'pointer': t2Phase
	},
	'2lossy': {
		'num_args': 4,
		'pointer': t2Lossy
	},
	'2bms': {
		'num_args': 2,
		'pointer': t2BMS
	},
	'1bms2': {
		'num_args': 1,
		'pointer': t1BMS2
	},
	'1phase2': {
		'num_args': 2,
		'pointer': t1Phase2
	},
	'1lossy2': {
		'num_args': 2,
		'pointer': t1Lossy2
	},
	'1bmsM': {
		'num_args': 1,
		'pointer': t1BMSM
	},
	'1lossyM': {
		'num_args': 2,
		'pointer': t1LossyM
	},
	'1phaseM': {
		'num_args': 2,
		'pointer': t1PhaseM
	}
}

# Общий класс всех гейтов оптического чипа реализующий их преобразование
class Transformation:
	def set(self, arguments):
		# self.transform = np.kron(np.kron(
		# 	np.eye(int(m.pow(2, self.inlet - 1))),
		# 	self.transform_matrix_func(arguments)),
		# 	np.eye(int(m.pow(2, self.chip_dimension - self.inlet)))
		# )
		self.transform = self.transform_matrix_func(arguments)

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
	
	
class OpticalTransformation:
	'''
	Optical transformation
 	'''
  
	def __init__(self,
              	 hFunc,
              	 size		: int,
                 id			: id	= 0,
                 bounds		: tuple	= None,
              	 name		: str	= "unnamed", 
              	 argsNum	: int	= 0,
              	 position	: int	= 0,
              	 isDistor	: bool	= False		) -> None:
		'''
		hFunc 		- Handel to a function which return matrix of the optical transformation.
		inletsNum	- Number of inlets for the optical transformation.
		name 		- Name of the optical transformation.
		argsNum 	- Number of necessary arguments for the function hFunc.
		inlets		- List of which inlets the optical transformation must affect on.
		isDistor	- Flag, True if transformation distor state in optical scheme.
		'''
		# Init all class fields
		self._hFunc 	= hFunc
		self._size		= size
		self._id		= id
		self._bounds	= bounds
		self._name 		= name
		self._argsNum	= argsNum
		self._position	= position
		self._isDistor	= isDistor
		self._args		= None	# Transformation arguments
		self._matrix	= None 	# Transformation matrix
  
		# Init info class fields
		self.__class_name	: str	= "Class::OpticalTransformation"
		self.__class_ver	: str	= "0.1"
			

	def __call__(self, inState: np.array) -> np.array:
		# if (self._matrix == None):
		# 	raise ValueError (
		# 		f"Error in {self.__class_name}::__call__ (ver: {self.__class_ver}) with parameter 'self._matrix'. " +
		# 		f"Матрица оптического преобразования '{self._name}' не определена!"
		# 	)
   
		outState = np.dot(self._matrix, inState)
  
		return outState
  
	def setArgs(self, args: list()) -> None:
		if (len(args) != self._argsNum):
			raise ValueError(
				f"Error in {self.__class_name}::setArgs (ver: {self.__class_ver}) with parameter 'args'. " +
				"Передано неверное количество аргументов квантового преобразования " +
				f"'{self._name}': {len(args)} вместо {self._argsNum}!"
			)
		
		self._args		= args
		self._matrix 	= self._hFunc(args)
  
	def getMatrix(self, chipSize=None):
		if (not self._matrix.any()):
			raise ValueError (
				f"Error in {self.__class_name}::getMatrix (ver: {self.__class_ver}) with parameter 'self._matrix'. " +
				f"Матрица оптического преобразования '{self._name}' не определена!"
			)
     
		if (chipSize == None or chipSize == self._size):
			return self._matrix
   
		before			= self._position
		last 			= self._position + self._size
		after 			= chipSize - last
		expandMatrix 	= np.pad(self._matrix, ((before,after),(before,after)), mode='constant', constant_values=0)
		expandMatrix[range(before), range(before)] = 1
		expandMatrix[range(last, chipSize), range(last, chipSize)] = 1
  
		return expandMatrix

	def getInfo(self) -> dict:
		info : dict = {
			'name' 		: self._name,
			'id'		: self._id,
			'args'		: self._args,
			'bounds'	: self._bounds,
			'position'	: self._position,
			'size'		: self._size
		}
  
		return info
   
	def copy(self):
		return copy.deepcopy(self)
	
	
# Относительная фазовая задержка
def tfPhaseRel_2(args):
	p = args[0]
	
	u = np.array(
		[[1, 	0		],
		 [0, 	cm.exp(1j*p)]],
		dtype=complex
	)
	
	return u

def tfPhaseAll_2(args):
    p0 = args[0]
    p1 = args[1]
    
    u = np.array(
		[[cm.exp(1j*p0), 	0				],
		 [0, 				cm.exp(1j*p1)	]],
		dtype=complex
	)
    
    return u

# Потери в каналах
def tfLossy_2(args):
	t0 = args[0]
	t1 = args[1]
	
	u = np.array(
		[[m.sqrt(t0), 0			],
		 [0,		 m.sqrt(t1)	]],
		dtype=complex
	)
	
	return u

# Не поляр. светоделитель
def tfBMS_2(args):
	r = args[0]

	u = np.array(
		[[m.sqrt(r),  -m.sqrt(1-r) ],
		 [m.sqrt(1-r), m.sqrt(r)   ]],
		dtype=complex
	)

	return u

# 
def tfPhase_4(args):
	p0 = args[0]
	p1 = args[1]
	p2 = args[2]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, cm.exp(1j*p0), 0, 0],
		 [0, 0, cm.exp(1j*p1), 0],
		 [0, 0, 0, cm.exp(1j*p2)]],
		dtype=complex
	)
	
	return u

# 
def tfLossy_4(args):
	t0 = args[0]
	t1 = args[1]
	t2 = args[2]
	t3 = args[3]
	
	u = np.array(
		[[m.sqrt(t0), 0, 0, 0],
		 [0, m.sqrt(t1), 0, 0],
		 [0, 0, m.sqrt(t2), 0],
		 [0, 0, 0, m.sqrt(t3)]],
		dtype=complex
	)
	
	return u

# 
def tfBMS_4(args):
	r0 = args[0]
	r1 = args[1]
	
	u = np.array(
		[[m.sqrt(r0), -m.sqrt(1-r0), 0, 0],
		 [m.sqrt(1-r0), m.sqrt(r0), 0, 0],
		 [0, 0, m.sqrt(r1), -m.sqrt(1-r1)],
		 [0, 0, m.sqrt(1-r1), m.sqrt(r1)]],
		dtype=complex
	)
	
	return u

# 
def tfBMS_2_2(arguments):
	r = arguments[0]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, 1, 0, 0],
		 [0, 0, m.sqrt(r), -m.sqrt(1-r)],
		 [0, 0, m.sqrt(1-r), m.sqrt(r)]],
		dtype=complex
	)
	
	return u

# 
def tfPhase_2_2(arguments):
	p0 = arguments[0]
	p1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, 1, 0, 0],
		 [0, 0, cm.exp(1j*p0), 0],
		 [0, 0, 0, cm.exp(1j*p1)]],
		dtype=complex
	)
	
	return u


# 
def tfPhase_2_0(arguments):
	p0 = arguments[0]
	p1 = arguments[1]
	
	u = np.array(
		[[cm.exp(1j*p0), 0, 0, 0],
		 [0, cm.exp(1j*p1), 0, 0],
		 [0, 0, 1, 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u

# 
def tfLossy_2_2(arguments):
	t0 = arguments[0]
	t1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, 1, 0, 0],
		 [0, 0, m.sqrt(t0), 0],
		 [0, 0, 0, m.sqrt(t1)]],
		dtype=complex
	)
	
	return u

# 
def tfBMS_2_1(arguments):
	r = arguments[0]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, m.sqrt(r), -m.sqrt(1-r), 0],
		 [0, m.sqrt(1-r), m.sqrt(r), 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u

# 
def tfPhase_2_1(arguments):
	p0 = arguments[0]
	p1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, cm.exp(1j*p0), 0, 0],
		 [0, 0, cm.exp(1j*p1), 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u

# 
def tfLossy_2_1(arguments):
	t0 = arguments[0]
	t1 = arguments[1]
	
	u = np.array(
		[[1, 0, 0, 0],
		 [0, m.sqrt(t0), 0, 0],
		 [0, 0, m.sqrt(t1), 0],
		 [0, 0, 0, 1]],
		dtype=complex
	)
	
	return u
 
hOTphase_2		= OpticalTransformation(tfPhaseRel_2,	2,	name='phase_2', 	argsNum=1, isDistor=True				)
hOTlossy_2		= OpticalTransformation(tfLossy_2, 		2,	name='lossy_2', 	argsNum=2, isDistor=True				)
hOTbms_2		= OpticalTransformation(tfBMS_2, 		2,	name='bms_2', 		argsNum=1, isDistor=False				)
hOTphase_4		= OpticalTransformation(tfPhase_4, 		4,	name='phase_4', 	argsNum=3, isDistor=True				)
hOTlossy_4		= OpticalTransformation(tfLossy_4, 		4,	name='lossy_4', 	argsNum=4, isDistor=True				)
hOTbms_4		= OpticalTransformation(tfBMS_4, 		4,	name='bms_4', 		argsNum=2, isDistor=False				)
hOTphase_2_2	= OpticalTransformation(tfPhase_2_2, 	4,	name='phase_2_2', 	argsNum=2, isDistor=True)
hOTlossy_2_2	= OpticalTransformation(tfLossy_2_2, 	4,	name='lossy_2_2', 	argsNum=2, isDistor=True)
hOTbms_2_2		= OpticalTransformation(tfBMS_2_2, 		4,	name='bms_2_2', 	argsNum=1, isDistor=False)
hOTphase_2_1	= OpticalTransformation(tfPhase_2_1, 	4,	name='phase_2_1', 	argsNum=2, isDistor=True)
hOTlossy_2_1	= OpticalTransformation(tfLossy_2_1, 	4,	name='lossy_2_1', 	argsNum=2, isDistor=True)
hOTbms_2_1		= OpticalTransformation(tfBMS_2_1, 		4,	name='bms_2_1', 	argsNum=1, isDistor=False)




