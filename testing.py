# Подключение общих модулей
import sys

# Подключение пользовательских модулей
# из папки package
import package.data_files as df
import package.functions as fn
import package.plot as plt



# Начало исполнения скрипта тестирования
if __name__ == '__main__':
	
	test_param = {
		'volume': int(5e3),
		'regime': 'n'
	}

	# Считывание путей к .dat файлам из аргументов, который будет тестироваться
	dir_pass = sys.argv[1:]
	num = len(dir_pass)

	deviations = [list(), list(), list(), list(), list()]

	i: int = 0

	for dp in dir_pass:
		i += 1
		print("Testing " + str(i) + ": " + str(dp))

		# Взятие словаря info из файла и взятие из него необходимых параметров
		info = df.pullFromDataFile(dp)
		[chip, result_x] = fn.chipFromInfo(info)

		# Тестирование
		test_data = fn.generateData(chip, test_param['volume'], test_param['regime'])
		devs = fn.testingDeviation(chip, test_data, result_x)

		for j in range(len(deviations)):
			deviations[j] = [*deviations[j], *devs[j]]

		test_info = fn.calTestInfo(devs)
		info['test_param'] = test_param
		info['test_result'] = test_info

		df.pushToDataFile(info, dp, gendir=False)
		df.createInfoFile(info, dp)
	
	test_info = fn.calTestInfo(deviations)
	
	if num == 1:
		plt.plotHists(deviations, test_info, dir_pass[0])
	else:
		plt.plotHists(deviations, test_info, "./")
	
	
	
	
