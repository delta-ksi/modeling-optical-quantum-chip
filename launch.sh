#!/bin/bash

#@ Сделать всё через пул действий

# Флаги запуска отдельных модулей скрипта
tomf=false
tesf=false

# Создание директории с информацией о томографии
if [ "$(find -name 'data')" = '' ]; then
	mkdir data
fi

# Обработка опций скрипта
if [ $# -ne 0 ]; then
	for arg in "$@"
	do
		case $arg in
			# Тестирование
			-ts|--test)
				tesf=true 
			;;

			# Томография
			-tm|--tomography)
				tomf=true 
			;;

			# Удаление последнего файла
			-d|--delete)
				# Проверка, что пользователь действительно
				# хочет удалить файл
				flag=false
				read -p "WARNING::LAUNCH: You want to delete the last file in ./data? (yes/no): " ans

				case $ans in
				y|yes)
					flag=true
				;;
				*)
					echo "Cansel deleting. Exit script."
					exit 0
				;;
				esac

				if [ "$flag" = true ]; then
					# Нахождение последнего по времени созданного файла
					data_pass=$(ls ./data --sort time | head -n 1)

					# Обработка условия отсутствия хоть какого-нибудть файла данных
					if [ $data_pass != '' ]; then
						rm -f ./data/$data_pass
					else
						echo "ERROR::LAUNCH: Don't find any data file!"
						exit -1
					fi
				fi
			;;

			-D|--deleteall)
				# Проверка, что пользователь действительно
				# хочет удалить файл
				flag=false
				read -p "WARNING::LAUNCH: You want to delete ALL files in ./data? (yes/no): " ans

				case $ans in
				y|yes)
					flag=true
				;;
				*)
					echo "Cansel deleting. Exit script."
					exit 0
				;;
				esac

				if [ "$flag" = true ]; then
					rm -f ./data/*
				fi
			;;

			# Мануал
			-h|--help)
				echo "-tes or --testing: Using for testing tomographed chip (TC). It builds histogram, and adds to file new information about TC."
				echo "-tom or --tomography: Using for tomography chip. It uses method dif evolution for findng fixed parameters of transformations of chip."
				echo "-d or --delete: Delete the last file in ./data."
				echo "-D or --deleteall: Delete all files in ./data."
				exit 0
			;;

			# Ошибка
			*)
				echo "ERROR::LAUNCH: Unknow option $arg, please use --help for more information about script options!"
				exit -1
			;;
		esac
	done
else
	tomf=true
	tesf=true
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
	if [ "$data_pass" != '' ]; then
		# Запуск скрипта на тестирование стомографированного чипа.
		# Строит графики гистрограмм и дополняет .dat файл
		# новой статистической информацией
		echo "Data file ./data/$data_pass:"
		echo "Launch testing script..."
		python3 -B test.py "./data/$data_pass" &
	else
		echo "ERROR::LAUNCH: Don't find any data file!"
		exit -1
	fi
fi

# Удаление вспомогательных файлов python
if [ "$(find -name '__pycache__')" != '' ]; then
	rm -r __pycache__
fi





