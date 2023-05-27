# Подключение общих модулей
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

nbins: int = 30
nloc: int = 4

def plotHists(deviations, info: dict, dir_pass: str="") -> None:
    plt.style.use('_mpl-gallery-nogrid')

    fig = plt.figure(layout="constrained", figsize=(15, 7))
    subfigs = fig.subfigures(1, 2, width_ratios=[9, 11])

    axsL = subfigs[0].subplots(2, 2)

    axsL[0,0].axvspan(info['M[p]']-np.sqrt(info['D[p]']), info['M[p]']+np.sqrt(info['D[p]']), facecolor='#ffff00')
    axsL[0,0].hist(deviations[0] , bins=nbins)
    axsL[0,0].set_xlabel(r'$\Delta\rho$')
    axsL[0,0].set(xlim=[info['p_min'], info['p_max']])
    axsL[0,0].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL[0,0].xaxis.set_minor_locator(ticker.NullLocator())
    axsL[0,0].axvline(info['M[p]'], color='r')

    axsL[0,1].axvspan(info['M[pPr]']-np.sqrt(info['D[pPr]']), info['M[pPr]']+np.sqrt(info['D[pPr]']), facecolor='#ffff00')
    axsL[0,1].hist(deviations[1], bins=nbins)
    axsL[0,1].set_xlabel(r'$\Delta\rho_{pr}$')
    axsL[0,1].set(xlim=[info['pPr_min'], info['pPr_max']])
    axsL[0,1].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL[0,1].xaxis.set_minor_locator(ticker.NullLocator())
    axsL[0,1].axvline(info['M[pPr]'], color='r')
        
    axsL[1,0].axvspan(info['M[pT]']-np.sqrt(info['D[pT]']), info['M[pT]']+np.sqrt(info['D[pT]']), facecolor='#ffff00')
    axsL[1,0].hist(deviations[2] , bins=nbins)
    axsL[1,0].set_xlabel(r'$\Delta\rho_t$')
    axsL[1,0].set(xlim=[info['pT_min'], info['pT_max']])
    axsL[1,0].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL[1,0].xaxis.set_minor_locator(ticker.NullLocator())
    axsL[1,0].axvline(info['M[pT]'], color='r')

    axsL[1,1].axvspan(info['M[pTrel]']-1-np.sqrt(info['D[pTrel]']), info['M[pTrel]']-1+np.sqrt(info['D[pTrel]']), facecolor='#ffff00')
    axsL[1,1].hist(np.subtract(deviations[3],1), bins=nbins)
    axsL[1,1].set_xlabel(r'$\Delta\rho_{T_{rel}}-1$')
    axsL[1,1].set(xlim=[info['pTrel_min']-1, info['pTrel_max']-1])
    axsL[1,1].xaxis.set_major_locator(ticker.MaxNLocator(nloc))
    axsL[1,1].xaxis.set_minor_locator(ticker.NullLocator())
    axsL[1,1].axvline(info['M[pTrel]']-1, color='r')

    axsR = subfigs[1].subplots()

    maxX = info['pPr_max'] / 1.0
    maxY = info['pT_max'] / 1.0
    ddX = maxX / 30
    ddY = maxY / 30

    # cmap = copy(plt.cm.plasma)
    # cmap.set_bad(cmap(0))
    # ... cmap=cmap ...
    # axsR.scatter(deviations[1], deviations[2])
    h_hist = axsR.hist2d(deviations[1], deviations[2], bins=(np.arange(0, maxX+ddX/10, ddX), np.arange(0, maxY+ddY/10, ddY)))
    plt.colorbar(h_hist[3], ax=axsR, extend='max')
    axsR.scatter(info['M[pPr]'], info['M[pT]'], marker='x', c='r', s=100)
    axsR.set_xlabel(r'$\Delta\rho_{pr}$')
    axsR.set_ylabel(r'$\Delta\rho_t$')
    axsR.set(xlim=(0, maxX), ylim=(0, maxY))

    if dir_pass != "":
        plt.savefig(dir_pass + '/plot.png')
        plt.savefig(dir_pass + '/plot.pdf')

    plt.show()
	