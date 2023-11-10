import package.data_files as df

if __name__ == "__main__":
	dir_pass = "result/20230811_215923"

	info = df.pullFromDataFile(dir_pass)
	result_x = info['charac_result']['result.x']
	transformations	= info['chip_info']['transforms']
	
	k = 0
	for i in range(len(transformations)):
		transform	= transformations[i]
		name		= transform['name']
		parameters	= transform['parameters']
		unfixed		= transform['unfixed']
		
		if unfixed:	
			print(name + "\t[" + "Unfixed" + "]\t" + "Unfixed")
		else:
			tmp = ""
			tmp1 = ""
			for j in range(len(parameters)):
				tmp += str(f'{parameters[j]:.{6}f}') + " "
				tmp1 += str(f'{result_x[k]:.{6}f}') + " "
				k += 1
				
			print(name + "\t[" + tmp + "]\t" + tmp1)
			# if (len(parameters) == 1): k += 1
