# Подключение общих модулей
import matplotlib.pyplot as plt
import numpy as np


def plotHists(deviations, info):
    fig, ax = plt.subplots(1, 4, sharey=True, tight_layout=True, figsize=(16, 4))
        
    ax[0].hist(deviations[0] , bins=30)
    ax[0].set_xlabel(r'$\Delta\rho$')
    ax[0].set_ylabel('NUMBER')

    ax[1].hist(deviations[1], bins=30)
    ax[1].set_xlabel(r'$\Delta\rho_{pr}$')
        
    ax[2].hist(deviations[2] , bins=30)
    ax[2].set_xlabel(r'$\Delta\rho_t$')

    ax[3].hist(np.subtract(deviations[3], 1) , bins=30)
    ax[3].set_xlabel(r'$\Delta\rho_{T_{rel}}-1$')

    ax[0].vlines([info['M[p]']], 0, 1, transform=ax[0].get_xaxis_transform(), color='r')
    ax[1].vlines([info['M[pPr]']], 0, 1, transform=ax[1].get_xaxis_transform(), color='r')
    ax[2].vlines([info['M[pT]']], 0, 1, transform=ax[2].get_xaxis_transform(),  color='r')
    ax[3].vlines([info['M[pTrel]']-1], 0, 1, transform=ax[3].get_xaxis_transform(), color='r')

    plt.show()
	