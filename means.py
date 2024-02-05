# Подключение общих модулей
import sys
import matplotlib.pyplot as plt
import numpy as np

# Подключение пользовательских модулей
# из папки package
import package.data_files as df



# Начало исполнения скрипта
if __name__ == '__main__':
    
    #
    dirPass:list = sys.argv[1:]

    noise   = list()
    MpPr    = list()
    MpT     = list()

    # Взятие словаря info из файла и взятие из него необходимых параметров
    for dp in dirPass:
        testResult = df.pullFromDataFile(dp, "testing-result")
        charResult = df.pullFromDataFile(dp, "characterization-result")
        noise_ = charResult['parameters']['noise']
        MpPr_ = testResult['statistical-info']['M[pPr]']
        MpT_ = testResult['statistical-info']['M[pT]']
        
        # print(f"{dp}: {noise_} | {MpPr_} | {MpT_}")
        noise.append(noise_)
        MpPr.append(MpPr_)
        MpT.append(MpT_)

    l_noise = np.log(noise)
    l_MpPr = np.log(MpPr)
    l_MpT = np.log(MpT)

    d = np.mean(np.power(l_noise,2))-np.power(np.mean(l_noise),2)
    b_pT = (np.mean(np.multiply(l_MpT, l_noise))-np.mean(l_MpT)*np.mean(l_noise)) / d
    a_pT = np.mean(l_MpT) - b_pT*np.mean(l_noise)

    b_pPr = (np.mean(np.multiply(l_MpPr, l_noise))-np.mean(l_MpPr)*np.mean(l_noise)) / d
    a_pPr = np.mean(l_MpPr) - b_pPr*np.mean(l_noise)

    x =     [np.min(noise),     np.max(noise)   ]
    y_pT =  [np.exp(b_pT *np.min(l_noise)+a_pT),   np.exp(b_pT *np.max(l_noise)+a_pT) ]
    y_pPr = [np.exp(b_pPr*np.min(l_noise)+a_pPr),  np.exp(b_pPr*np.max(l_noise)+a_pPr)]

    fig = plt.figure(layout="constrained", figsize=(8, 4))
    ax = fig.subplots(1, 2, sharex=True, sharey=True)

    ax[0].plot(noise, MpPr, 'bx')
    ax[0].plot(x, y_pPr, 'r')
    ax[0].set_xlabel('noise')
    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    ax[0].set_title(r'$M[\Delta\rho_{Pr}]$')

    ax[1].plot(noise, MpT, 'bx')
    ax[1].plot(x, y_pT, 'r')
    ax[1].set_xlabel('noise')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].set_title(r'$M[\Delta\rho_T]$')

    plt.show()
    
     
