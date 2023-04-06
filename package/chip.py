# Подключение общих модулей
import copy
import numpy as np

# Подключение пользовательских модулей
from . import transformation as tf



# Класс оптического чипа
class Chip:

	def __init__(self, chip_dimension, noise=0):
		self.transformations = list()
		self.fixed_transforms = list()
		self.unfixed_transforms = list()
		self.chip_dimension = chip_dimension
		self.noise = noise
		


	def set(self, name_tran_mat_fun, inlet, params, bounds, unfixed=False):
		tid = len(self.transformations)
		
		transform = tf.Transformation(
			tid,
			name_tran_mat_fun,
			[self.chip_dimension, inlet],
			params,
			bounds
		)
		
		if unfixed == True:
			self.unfixed_transforms.append(tid)
		else:
			self.fixed_transforms.append(tid)
			
		self.transformations.append(transform)
		


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
		


	def compute(self, in_state, return_unnoise_too=False):
		# Инициализация выходного состояния
		out_state = in_state
		
		for t in self.transformations:
			out_state = t(out_state)
			
		if self.noise != 0:
			out_state_unnoised = out_state.copy()
			out_state_mistake = np.abs(np.random.normal(0, self.noise, [2,1]))
			out_state += out_state*out_state_mistake
		
		if return_unnoise_too:
			return [out_state, out_state_unnoised]
		else:
			return out_state
		


	def getFixedParamBounds(self):
		bounds = ()
		for t in self.transformations:
			if self.unfixed_transforms.count(t.id) == 0:
				bounds = (*bounds, *t.bounds)
			
		return bounds
	


	def getChipSetupInfo(self):
		info = dict()
		
		info['dimention'] = self.chip_dimension
		info['noise'] = self.noise
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





