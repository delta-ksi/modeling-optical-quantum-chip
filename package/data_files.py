# Подключение общих модулей
import datetime
import pickle
import pprint
import os



def createDataDir(dirPass : str,
                  dirName : str = None) -> str:
    nowData     : datetime  = datetime.datetime.today()
    dirName     : str       = nowData.strftime('%Y%m%d-%H%M%S') if dirName == None else dirName
    newDirPass  : str       = dirPass + '/' + dirName
    os.makedirs(newDirPass)
    return newDirPass    



def pushToTextFile(info         : dict,
                   dirPass      : str,
                   fileName     : str   = "unnamed") -> None:
    
    filePass    : str = dirPass + '/' + fileName
    text        : str = pprint.pformat(info)

    with open(filePass, 'wt') as fout:
        fout.write(text)



def pushToDataFile(info         : dict,
                   dirPass      : str,
                   fileName     : str   = "unnamed") -> None:

    filePass    : str  = dirPass + '/' + fileName + '.pickle'
    
    with open(filePass, 'wb') as fout:
        pickle.dump(info, fout)



def pullFromDataFile(dirPass : str,
                     fileName: str) -> dict:

    filePass = dirPass + '/' + fileName + '.pickle'

    info = dict()
    with open(filePass, 'rb') as fin:
        info = pickle.load(fin)
	
    return info




