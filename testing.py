# Подключение всех необходимых библиотек

import sys
import pickle
import matplotlib.pyplot as plt

import chip as ch
import functions as fn

def testingDeviation(chip, test_data, pred_params):
	
	tchip = chip.copy()
	tchip.changeFixedParams(pred_params)
	
	deviate = list()
	deviate_pr = list()
	deviate_t = list()
	
		
	for data in test_data:			
		
		[dev, dev_pr, dev_t] = fn.getDeviation(tchip, [data])
	
		deviate.append(dev)
		deviate_pr.append(dev_pr)
		deviate_t.append(dev_t)
	
	return [deviate, deviate_pr, deviate_t]

# Начало исполнения скрипта
if __name__ == '__main__':
	
	file_pass = sys.argv[1]
	
	data = dict()
	
	# Запись всех данных моделирования в файл
	with open(file_pass, 'rb')	as f:
		data = pickle.load(f)
	
	result_x = data['model_result']['result.x']
	chip_dim = data['chip_info']['dimention']
	noise = data['chip_info']['noise']
	N = len(data['chip_info']['transforms'])
	
	chip = ch.Chip(chip_dim, noise)
	
	for i in range(N):
		name = data['chip_info']['transforms'][i]['name']
		inlet = data['chip_info']['transforms'][i]['inlet']
		parameters = data['chip_info']['transforms'][i]['parameters']
		bounds = data['chip_info']['transforms'][i]['bounds']
		unfixed_ = data['chip_info']['transforms'][i]['unfixed']
		chip.set(name, inlet, parameters, bounds, unfixed=unfixed_)
		
	pChip = chip.copy()
	result_x = data['model_result']['result.x']
	
	# Тестирование
	test_data = fn.generateData(chip, 10000,  input_norm_dis=False)
	[deviation, deviation_pr, deviation_t] = testingDeviation(chip, test_data, result_x)
	
	fig, ax = plt.subplots(1, 3, sharey=True, tight_layout=True, figsize=(12, 5))
	
	ax[0].hist(deviation , bins=30)
	ax[0].set_xlabel(r'$\Delta\rho$')
	ax[0].set_ylabel('NUMBER')
	
	ax[1].hist(deviation_pr, bins=30)
	ax[1].set_xlabel(r'$\Delta\rho_{pr}$')
	
	ax[2].hist(deviation_t , bins=30)
	ax[2].set_xlabel(r'$\Delta\rho_t$')
	
	plt.show()
	
	
	
	
	
	
	
	
	
	
	
	
