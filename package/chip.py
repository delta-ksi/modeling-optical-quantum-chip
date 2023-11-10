# Подключение общих модулей
import copy
import numpy as np

# Подключение пользовательских модулей
from . import transformation as tf



# Класс оптического чипа
class Chip:

	def __init__(self, dimension):
		self.transformations = list()
		self.fixed_transforms = list()
		self.unfixed_transforms = list()
		self.dimension = dimension
		self.args = list()
		


	def set(self, name_tran_mat_fun, inlet, params, bounds, unfixed=False):
		tid = len(self.transformations)
		
		if len(params) == 0:
			for i in range(len(bounds)):
				number = float(np.random.uniform(bounds[i][0], bounds[i][1], 1))
				params = [*params, number]
				self.args.append(number)

		transform = tf.Transformation(
			tid,
			name_tran_mat_fun,
			[self.dimension, inlet],
			params,
			bounds
		)
		
		if unfixed == True:
			self.unfixed_transforms.append(tid)
		else:
			self.fixed_transforms.append(tid)
			
		self.transformations.append(transform)
		
	def getArgs(self):
		return self.args

	def changeUnfixedParams(self, params):
		j = 0
		for i in self.unfixed_transforms:
			args = []
			num_of_params = self.transformations[i].transform_info['num_args']
			
			for k in range(num_of_params):
				args = [*args,params[j]]
				j += 1
			
			self.transformations[i].set(args)
			


	def changeFixedParams(self, params):
		j = 0
		for i in self.fixed_transforms:
			args = []
			num_of_params = self.transformations[i].transform_info['num_args']
			
			for k in range(num_of_params):
				args = [*args,params[j]]
				j += 1

			self.transformations[i].set(args)
		


	def compute(self, in_state: np.array):
		# Инициализация выходного состояния
		out_state = in_state.copy()

		for t in self.transformations:
			out_state = t(out_state)
		
		return out_state
		


	def getFixedParamBounds(self) -> tuple:
		bounds = ()
		for t in self.transformations:
			if self.unfixed_transforms.count(t.id) == 0:
				bounds = (*bounds, *t.bounds)
			
		return bounds

	def getChipSetupInfo(self) -> dict:
		info = dict()
		
		info['dimention'] = self.dimension
		info['transforms'] = {}
		for t in self.transformations:
			unfixed = False
			if self.unfixed_transforms.count(t.id) != 0:
				unfixed = True
				
			transform_info = t.transform_info
			transform_info['unfixed'] = unfixed
			
			info['transforms'][t.id] = transform_info
			
		return info



	def copy(self):
		return copy.deepcopy(self)


class OpticalChip:
	'''
	Optical chip
	'''
	
	def __init__(self,
              	 chipSize	: int,
                 name		: str = 'unnamed') -> None:
     	# Init all class fields
		self._chipSize 					= chipSize
		self._name						= name
		self._transformations			= list()
		self._unfixedTransformations	= list()
		self._fixedTransformations		= list()

	def newTransformation(self,
                       	  transformation	: tf.OpticalTransformation,
         				  args 				: list | float				= None,
          				  bounds			: tuple						= None,
           				  unfixed			: bool						= False) -> None:
     
		id = len(self._transformations)
		
		if (args == None):
			if (bounds != None):
				args = [float(np.random.uniform(i[0], i[1], 1)) for i in bounds]
				transformation.setArgs(args)
		else:
			transformation.setArgs(args)
			
		transformation._id		= id
		transformation._args	= args
		transformation._bounds	= bounds
  
		# Set new atribute to OpticalTransformation class
		setattr(transformation, '_unfixed', unfixed)
    
		if unfixed:
			self._unfixedTransformations.append(id)
		else:
			self._fixedTransformations.append(id)
			
		self._transformations.append(transformation.copy())

	def changeUnfixedArgs(self, args: list):
		j : int = 0
		for i in self._unfixedTransformations:
			argsNum = self._transformations[i]._argsNum
			self._transformations[i].setArgs([args[k] for k in range(j, j+argsNum)])
			j = j + argsNum

	def changeFixedArgs(self, args: list):
		j : int = 0
		for i in self._fixedTransformations:
			argsNum = self._transformations[i]._argsNum
			self._transformations[i].setArgs([args[k] for k in range(j, j+argsNum)])
			j = j + argsNum
   
	def changeArgs(self, args: list):
		j : int = 0
		for i in range(len(self._transformations)):
			argsNum = self._transformations[i]._argsNum
			self._transformations[i].setArgs([args[k] for k in range(j, j+argsNum)])
			j = j + argsNum
   
	def getFixedArgsBounds(self) -> tuple:
		return tuple(self._transformations[i]._bounds[j]
               			for i in self._fixedTransformations
                  			for j in range(self._transformations[i]._argsNum))

   
	def getChipTransformation(self) -> np.array:
		if (len(self._transformations) == 1):
			return self._transformations[0].getMatrix(self._chipSize)
  
		return np.linalg.multi_dot([i.getMatrix(self._chipSize) for i in self._transformations[::-1]])

	def genChipInfo(self) -> dict:
		info = dict()
		
		# Init main dict fields
		info['name']						: str	= self._name
		info['size'] 						: int 	= self._chipSize
		info['transformations'] 			: dict 	= dict()
  
		# Fill fields
		info['transformations']['number'] 	: int	= len(self._transformations)
		for t in self._transformations:
			transformationInfo 				: dict 	= t.getInfo()
			transformationInfo['unfixed']	: bool	= t._unfixed
			info['transformations'][t._id] 	: dict	= transformationInfo
			
		return info

	def compute(self, inState: np.array):
		# Инициализация выходного состояния
		outState = inState.copy()

		for t in self._transformations:
			outState = t(outState)
		
		return outState
		
	def copy(self):
		return copy.deepcopy(self)

		



