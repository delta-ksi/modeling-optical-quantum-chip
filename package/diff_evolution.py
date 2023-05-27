# Подключение общих модулей
import time
import scipy.optimize as sp_opt

# Подключение пользовательских модулей
from . import functions as fn
from . import chip as ch

# Количество попыток алгоритма
N: int = 5
	
def minimizeFunction(optimize_params: list, args: list):
	chip:ch.Chip = args[0].copy()
	train_data = args[1]
	
	chip.changeFixedParams(optimize_params)
	
	deviations = fn.getDeviation(chip, train_data)

	return deviations[0]
	


def differentialEvolution(chip:ch.Chip, train_data:list(), params:dict(), display=False, print_info=True):
	
	# Начало отсчёта времени моделирования
	timer = time.perf_counter()

	attempt = 0

	for i in range(N):
		if print_info:
			print ("Start atempt " + str(i) + ": ", end='')

		attempt = i+1

		result = sp_opt.differential_evolution(
			func=minimizeFunction,
			bounds=chip.getFixedParamBounds(),
			args=[[chip.copy(), train_data]],
			strategy=params['strategy'],
			maxiter=params['maxiter'],
			tol=params['tol'],
			popsize=params['popsize'],
			mutation=params['mutation'],
			recombination=params['recombination'],
			workers=-1,
			updating='deferred',
			disp=display
		)

		if print_info:
			if result.success:
				print("Success")
				break
			else:
				print("Fail")

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
	
	
	
	
	
