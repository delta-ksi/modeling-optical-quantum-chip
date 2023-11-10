# Подключение общих модулей
import time
import scipy.optimize as sp_opt

# Подключение пользовательских модулей
from . import functions as fn
from . import chip as ch

# Максимальное количество попыток алгоритма
N: int = 1
	
def minimizeFunction(optimize_params: list, args: list):
	chip:ch.Chip = args[0].copy()
	train_data = args[1]
	
	chip.changeFixedParams(optimize_params)
	deviations = fn.getDeviation(chip, train_data)

	return deviations[0]

def minimizeFunction2(optimizeParameters: list, args: list):
	chip:ch.OpticalChip = args[0].copy()
	trainData 			= args[1]
	
	chip.changeFixedArgs(optimizeParameters)
 
	deviation = fn.getTrainDeviation(chip, trainData)

	return deviation


def differentialEvolution(chip:ch.Chip, train_data:list(), params:dict(), display=False, print_info=True):
	
	# Начало отсчёта времени моделирования
	timer = time.perf_counter()

	attempt = 0

	for i in range(N):
		attempt = i+1
     
		if print_info:
			if display:
				print (f"Start atempt {attempt}:")
			else:
				print (f"Start atempt {attempt}: ", end='')

		result = sp_opt.differential_evolution(
			func			= minimizeFunction,
			bounds			= chip.getFixedParamBounds(),
			args			= [[chip.copy(), train_data]],
			strategy		= params['strategy'],
			maxiter			= params['maxiter'],
			tol				= params['tol'],
			popsize			= params['popsize'],
			mutation		= params['mutation'],
			recombination	= params['recombination'],
			workers			= -1,
			updating		= 'deferred',
			disp			= display
		)

		if print_info:
			if result.success:
				if (result.fun < 10*params['noise']):
					print("Success")
					break
				else:
					print("Fail: High error rate")
			else:
				print("Fail: Too many iterations")

	# Окончание отсчёта времени моделирования
	timer = int(time.perf_counter() - timer)
	
	if print_info:
		# Вывод части данных томографии в консоль
		print(
			"time: " + str(timer) + " sec\n" + 
			"nit: " + str(result.nit) + "\n" +
			"fun: " + str(result.fun)
		)
	
	return [result, timer, attempt]
	
	
def differentialEvolution2(chip			: ch.OpticalChip,
                           data			: list(),
                           params		: dict(),
                           display		= False,
                           log			= True):
	
	# Начало отсчёта времени моделирования
	timer = time.perf_counter()

	attempt = 0

	for i in range(N):
		attempt = i+1
     
		if log:
			if display:
				print (f"Start atempt {attempt}:")
			else:
				print (f"Start atempt {attempt}: ", end='')

		result = sp_opt.differential_evolution(
			func			= minimizeFunction2,
			bounds			= chip.getFixedArgsBounds(),
			args			= [[chip.copy(), data]],
			strategy		= params['strategy'],
			maxiter			= params['maxiter'],
			tol				= params['tol'],
			popsize			= params['popsize'],
			mutation		= params['mutation'],
			recombination	= params['recombination'],
			workers			= -1,
			updating		= 'deferred',
			disp			= display
		)

		if log:
			if result.success:
				if (result.fun < 10*params['noise']):
					print("Success")
					break
				else:
					print("Fail: High error rate")
			else:
				print("Fail: Too many iterations")

	# Окончание отсчёта времени моделирования
	timer = int(time.perf_counter() - timer)
	
	if log:
		# Вывод части данных томографии в консоль
		print(
			"time: " + str(timer) + " sec\n" + 
			"nit: " + str(result.nit) + "\n" +
			"fun: " + str(result.fun)
		)
	
	return [result, timer, attempt]
	
	
