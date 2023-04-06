# Подключение общих модулей
import sys
import pprint

# Подключение пользовательских модулей
# из папки package
import package.functions as fn
import package.plot as plt



# Начало исполнения скрипта
if __name__ == '__main__':
	
	test_param = {
		'test_volume': 10000,
		'input_norm': False 
	}

	# Считывание пути к .dat файлу из аргументов, который будет тестироваться
	file_pass = sys.argv[1]

	# Взятие словаря info из файла и взятие из него словаря info
	info = fn.pullFromFile(file_pass)
	[chip, result_x] = fn.chipFromInfo(info)

	# Тестирование
	test_data = fn.generateData(chip, test_param['test_volume'], test_param['input_norm'])
	deviations = fn.testingDeviation(chip, test_data, result_x)

	test_info = fn.calTestInfo(deviations)
	info['test_param'] = test_param
	info['test_result'] = test_info
	
	print('\n')
	pp = pprint.PrettyPrinter()
	pp.pprint(info)

	fn.pushToFile(info, file_pass,gen=False)

	plt.plotHists(deviations, test_info)
	
	
	
	
	