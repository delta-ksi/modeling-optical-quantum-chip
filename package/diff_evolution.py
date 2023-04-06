# Подключение общих модулей
import time
import scipy.optimize as sp_opt

# Подключение пользовательских модулей
from . import functions as fn
	

	
def minimizeFunction(optimize_params, args):
	chip = args[0]
	train_data = args[1]
	
	chip.changeFixedParams(optimize_params)
	
	deviations = fn.getDeviation(chip, train_data)

	return deviations[0]
	
def differentialEvolution(chip, train_data, params, display=False, print_data=True):
	
	# Начало отсчёта времени моделирования
	timer = time.perf_counter()

	for i in range(3):
		print ("Start atempt " + str(i) + ": ", end='')
	
		result = sp_opt.differential_evolution(
			func=minimizeFunction,
			bounds=chip.getFixedParamBounds(),
			args=[[chip.copy(), train_data]],
			strategy=params['strategy'],
			maxiter=params['maxiter'],
			tol=params['tol'],
			atol=params['atol'],
			popsize=params['popsize'],
			mutation=params['mutation'],
			recombination=params['recombination'],
			workers=-1,
			updating='deferred',
			disp=display
		)

		if result.success:
			print("Success")
			break
		else:
			print("Fail")

	# Окончание отсчёта времени моделирования
	timer = time.perf_counter() - timer
	
	if print_data:
		# Вывод части данных томографии в консоль
		print(
			"time: " + str(timer) + " sec\n" + 
			"nit: " + str(result.nit) + "\n" +
			"fun: " + str(result.fun)
		)
	
	return [result, timer]
	
	
	
	
	
