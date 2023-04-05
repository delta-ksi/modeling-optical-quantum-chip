#!/bin/bash

# Флаги запуска отдельных
# модулей скрипта
tomf=false
tesf=false

# Обработка опций скрипта
if [ $# -ne 0 ]; then
	for arg in "$@"
	do
		case $arg in
			# Тестирование
			-tes)
				tesf=true 
			;;
			--testing)
				tesf=true 
			;;
			# Томография
			-tom)
				tomf=true 
			;;
			--tomography)
				tomf=true 
			;;
			# Мануал
			--help)
				echo "-tes or --testing: Using for testing tomographed chip (TC). It builds histogram, and adds to file new information about TC."
				echo "-tom or --tomography: Using for tomography chip. It uses method dif evolution for findng fixed parameters of transformations of chip."
				exit 0
			;;
			# Ошибка
			*)
				echo "Error: Unknow option or variable $arg, please use --help for more information about script options!"
				exit -1
			;;
		esac
	done
else
	tomf=true
	tesf=true
fi

# Создание директории с информацией о томографии
if [ "$(find -name 'data')" = '' ]; then
	mkdir data
fi

# Томография
if [ "$tomf" = true ]; then
	# Запуск скрипта на томографию оптического чипа.
	# В результате его работы будет создан файл,
	# содержащий информацию о томографии
	echo "Launch tomography script..."
	python3 -B tomography.py
fi

# Тестирование
if [ "$tesf" = true ]; then
	# Нахождение последнего по времени созданного файла,
	# который создал скрипт tomography.py
	data_pass=$(ls ./data --sort time | head -n 1)
	
	# Обработка условия отсутствия хоть какого-нибудть файла данных
	if [ $data_pass != '' ]; then
		# Запуск скрипта на тестирование стомографированного чипа.
		# Строит графики гистрограмм и дополняет .dat файл
		# новой статистической информацией
		echo "Data file ./data/$data_pass:"
		echo "Launch testing script..."
		python3 -B testing.py "./data/$data_pass" &
	else
		echo "Error: Don't find any data file!"
		exit -1
	fi
fi

# Удаление вспомогательных файлов
if [ "$(find -name '__pycache__')" != '' ]; then
	rm -r __pycache__
fi





