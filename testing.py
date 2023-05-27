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
		'volume': int(1e4),
		'regime': 'n'
	}

	# Считывание пути к .dat файлу из аргументов, который будет тестироваться
	dir_pass = sys.argv[1]

	# Взятие словаря info из файла и взятие из него необходимых параметров
	info = df.pullFromDataFile(dir_pass)
	[chip, result_x] = fn.chipFromInfo(info)

	# Тестирование
	test_data = fn.generateData(chip, test_param['volume'], test_param['regime'])
	deviations = fn.testingDeviation(chip, test_data, result_x)

	test_info = fn.calTestInfo(deviations)
	info['test_param'] = test_param
	info['test_result'] = test_info

	df.pushToDataFile(info, dir_pass, gendir=False)
	df.createInfoFile(info, dir_pass)

	plt.plotHists(deviations, test_info, dir_pass)
	
	
	
	
	