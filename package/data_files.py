# Подключение общих модулей
import datetime
import pickle
import pprint
import os



def pushToDataFile(info: dict, dir_pass: str="", gendir=True) -> None:

    # Создание директории
    if gendir:
            today: datetime = datetime.datetime.today()
            dir_pass: str   = dir_pass + '/' + today.strftime('%Y%m%d_%H%M%S')
            os.makedirs(dir_pass)

    if dir_pass != "":
        file_pass: str  = dir_pass + '/data'

        # Запись всех данных характеризации в файл
        with open(file_pass, 'wb') as fout:
            pickle.dump(info, fout)



def createInfoFile(info: dict, dir_pass: str="") -> None:

    if dir_pass != "":
        file_pass = dir_pass + '/info'

        output_s = pprint.pformat(info)

        # Запись всей информации о характеризации в файл
        with open(file_pass, 'wt') as fout:
            fout.write(output_s)



def pullFromDataFile(dir_pass: str, dir=True) -> dict:

    file_pass: str = ''

    if dir:
        file_pass = dir_pass + '/data'
    else: 
        file_pass = dir_pass

	# Чтение всех данных моделирования из файла
    data = dict()
    with open(file_pass, 'rb')	as fin:
        data = pickle.load(fin)
	
    return data




