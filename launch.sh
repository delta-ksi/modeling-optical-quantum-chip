#!/bin/bash

# Флаги запуска модулей скрипта
char_flag=false
test_flag=false
del_flag=false

# Основные переменные скрипта
data_folder_name=''
noise_val=''

# Создание директории ./result с информацией о томографии
if [ "$(find -name 'result')" = '' ]; then
	mkdir ./result
fi

tmp2=false
if [ "${1:0:1}" != '-' ]; then
	data_folder_name=$1
	tmp2=true
fi

# Обработка опций и аргументов скрипта
if [ $# -ne 0 ]; then
	for arg in "$@"
	do
		if [ '$tmp2' = true ]; then
			tmp2=false
		else
			case $arg in
				# Тестирование
				-t|--test)
					test_flag=true 
				;;

				# Характеризация
				-c|--characterization)
					char_flag=true 
				;;

				# Удаление последней папки с данными
				-d|--delete)
					# Проверка, что пользователь действительно хочет удалить файл
					read -p "WARNING::LAUNCH: You want to delete the last dir in ./result? (yes/no): " ans

					case $ans in
					y|yes|Y)
						del_flag=true
						if ['$data_folder_name' = '']; then
							# Нахождение последнего по времени созданного файла
							data_folder_name=$(ls ./result --sort time | head -n 1)
						fi
					;;
					*)
						echo "Cansel deleting. Exit script."
						exit 0
					;;
					esac
				;;

				# Удаление всех папок с данными
				-D|--deleteall)
					# Проверка, что пользователь действительно хочет удалить файл
					read -p "WARNING::LAUNCH: You want to delete ALL files in ./result? (yes/no): " ans

					case $ans in
					y|yes|Y)
						del_flag=true
						if [ $data_folder_name = '' ]; then
							# Удаление всех папок в директории ./result
							data_folder_name=*
						else
							# Удаление всех папок в директории ./result/"Указанная пользователем директория"
							data_folder_name='$data_folder_name/*'
						fi
					;;
					*)
						echo "Cansel deleting. Exit script."
						exit 0
					;;
					esac
				;;

				# Мануал
				-h|--help)
					echo "-t or --testing: Using for testing tomographed chip (TC). It builds histogram, and adds to file new information about TC."
					echo "-c or --characterization: Using for characterization chip. It uses method dif evolution for findng fixed parameters of transformations of chip."
					echo "-d or --delete: Delete the last data dir in ./result."
					echo "-D or --deleteall: Delete all data dirs in ./result."
					echo "-n: Insert noise into characterization.py script."
					exit 0
				;;

				# Введение шума
				-n*)
					noise_val=${arg:2}
				;;

				# Обработка ошибочной опции
				-*)
					echo "ERROR::LAUNCH: Unknow option $arg, please use --help for more information about script options!"
					echo "Leave launch.sh script..."
					exit -1
				;;
			esac
		fi
	done
fi

# Стандартный запуск скрипта
# Характеризация и затем тестирование полученного чипа
if ! $char_flag ; then
	if ! $test_flag ; then
		if ! $del_flag ; then
			char_flag=true
			test_flag=true
		fi
	fi
fi
	
: '
# Отладочный код
echo "char_flag = $char_flag"
echo "test_flag = $test_flag"
echo "del_flag = $del_flag"
echo "data_folder_name = $data_folder_name"
echo "noise = $noise_val"
# '

# : '
# Удаление папок данных
if $del_flag; then
	# Обработка условия отсутствия хоть какого-нибудть файла данных
	if [ '$delp' != '' ]; then
		echo "Start deleting..."
		rm -r --force ./result/$data_folder_name
		echo "Deleting complete! Exit script."
		exit 0
	else
		echo "ERROR::LAUNCH: Don't find any data file!"
		exit -1
	fi
fi

# Характеризация
if $char_flag; then

	data_dir="./result"
	if [ ! -z "$data_folder_name" ]; then
		data_dir="$data_dir/$data_folder_name"
	fi

	# Запуск скрипта на характеризацию оптического чипа.
	# В результате его работы будет создан data файл,
	# содержащий информацию о характеризации
	echo "Launch characterization script..."
	python3 characterization.py $data_dir $noise_val
fi

# Тестирование
if $test_flag; then
	# Нахождение последнего по времени созданной папки с данными,
	# который создал скрипт characterization.py
	if [ ${#data_folder_name} -eq 0 ]; then
		data_dir=$(ls ./result --sort time | head -n 1)
		data_dir=./result/$data_dir
	else
		data_dir=$(ls ./result/$data_folder_name --sort time | head -n 1)
		data_dir=./result/$data_folder_name/$data_dir
	fi

	# Обработка условия отсутствия какой-либо папки с данными
	if [ "$data_dir" != '' ]; then
		# Запуск скрипта на тестирование стомографированного чипа.
		# Строит и сохраняет графики гистрограмм, дополняет data файл
		# новой статистической информацией и создаёт текстовый info файл
		echo "Data dir: $data_dir"
		echo "Launch testing script..."
		python3 testing.py $data_dir
	else
		echo "ERROR::LAUNCH: Don't find any data dir!"
		exit -1
	fi
fi

echo "LAUNCH: EOF"

# Удаление вспомогательных файлов python
# pycache=$(find -name '__pycache__')
# if [ "$pycache" != '' ]; then
# 	rm -r $pycache
# fi

# '

