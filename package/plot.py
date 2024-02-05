# Подключение общих модулей
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

nbins:  int = 35    # Количество столбов в гистограмме
nloc:   int = 4     # Количество штрихов на коорд. оси
sig:    int = 3     # Количество сигм отклонений от медианы 

def range(name: str, info: dict):
    return [info[name+'_min'], np.min([info[name+'_max'], sig*np.sqrt(info['D['+name+']'])+info['M['+name+']']]) ]

def plotHists(deviations, info: dict, dirPass: str="") -> None:
    plt.style.use('_mpl-gallery-nogrid')

    fig = plt.figure(layout="constrained", figsize=(15, 7))
    subfigs = fig.subfigures(1, 2, width_ratios=[9, 11])

    outer = [['p', 'pPr'], ['pT', 'pPhase'], ['pTrel', 'pTrel']]
    axsL = subfigs[0].subplot_mosaic(outer)

    axsL['p'].axvspan(info['M[p]']-np.sqrt(info['D[p]']), info['M[p]']+np.sqrt(info['D[p]']), facecolor='#ffff00')
    axsL['p'].hist(deviations['D'] , bins=nbins, range=range('p', info))
    axsL['p'].set_xlabel(r'$\Delta\rho$')
    axsL['p'].set(xlim=range('p', info))
    axsL['p'].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL['p'].xaxis.set_minor_locator(ticker.NullLocator())
    axsL['p'].axvline(info['M[p]'], color='r')

    axsL['pPr'].axvspan(info['M[pPr]']-np.sqrt(info['D[pPr]']), info['M[pPr]']+np.sqrt(info['D[pPr]']), facecolor='#ffff00')
    axsL['pPr'].hist(deviations['Pr'], bins=nbins, range=range('pPr', info))
    axsL['pPr'].set_xlabel(r'$\Delta\rho_{pr}$')
    axsL['pPr'].set(xlim=range('pPr', info))
    axsL['pPr'].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL['pPr'].xaxis.set_minor_locator(ticker.NullLocator())
    axsL['pPr'].axvline(info['M[pPr]'], color='r')
        
    axsL['pT'].axvspan(info['M[pT]']-np.sqrt(info['D[pT]']), info['M[pT]']+np.sqrt(info['D[pT]']), facecolor='#ffff00')
    axsL['pT'].hist(deviations['T'] , bins=nbins, range=range('pT', info))
    axsL['pT'].set_xlabel(r'$\Delta\rho_t$')
    axsL['pT'].set(xlim=range('pT', info))
    axsL['pT'].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL['pT'].xaxis.set_minor_locator(ticker.NullLocator())
    axsL['pT'].axvline(info['M[pT]'], color='r')

    axsL['pTrel'].axvspan(info['M[pTrel]']-1-np.sqrt(info['D[pTrel]']), info['M[pTrel]']-1+np.sqrt(info['D[pTrel]']), facecolor='#ffff00')
    axsL['pTrel'].hist(np.subtract(deviations['Trel'],1), bins=nbins)
    axsL['pTrel'].set_xlabel(r'$\Delta\rho_{T_{rel}}-1$')
    axsL['pTrel'].set(xlim=[info['pTrel_min']-1, info['pTrel_max']-1])
    axsL['pTrel'].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL['pTrel'].xaxis.set_minor_locator(ticker.NullLocator())
    axsL['pTrel'].axvline(info['M[pTrel]']-1, color='r')

    axsL['pPhase'].axvspan(info['M[pPhase]']-np.sqrt(info['D[pPhase]']), info['M[pPhase]']+np.sqrt(info['D[pPhase]']), facecolor='#ffff00')
    axsL['pPhase'].hist(deviations['Phase'], bins=nbins, range=range('pPhase', info))
    axsL['pPhase'].set_xlabel(r'$\Delta\rho_{\phi}$')
    axsL['pPhase'].set(xlim=range('pPhase', info))
    axsL['pPhase'].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL['pPhase'].xaxis.set_minor_locator(ticker.NullLocator())
    axsL['pPhase'].axvline(info['M[pPhase]'], color='r')

    axsR = subfigs[1].subplots()

    maxX = np.min([info['pPr_max'], 2*np.sqrt(info['D[pPr]'])+info['M[pPr]']]) / 1.0
    maxY = np.min([info['pT_max'], 2*np.sqrt(info['D[pT]'])+info['M[pT]']]) / 1.0
    ddX = maxX / 30
    ddY = maxY / 30

    # cmap = copy(plt.cm.plasma)
    # cmap.set_bad(cmap(0))
    # ... cmap=cmap ...
    # axsR.scatter(deviations[1], deviations[2])
    h_hist = axsR.hist2d(deviations['Pr'], deviations['T'], bins=(np.arange(0, maxX+ddX/10, ddX), np.arange(0, maxY+ddY/10, ddY)))
    plt.colorbar(h_hist[3], ax=axsR, extend='max')
    axsR.scatter(info['M[pPr]'], info['M[pT]'], marker='x', c='r', s=100)
    axsR.set_xlabel(r'$\Delta\rho_{pr}$')
    axsR.set_ylabel(r'$\Delta\rho_t$')
    axsR.set(xlim=(0, maxX), ylim=(0, maxY))

    if dirPass != "":
        plt.savefig(dirPass + '/plot.png')
        plt.savefig(dirPass + '/plot.pdf')

    plt.show()
	