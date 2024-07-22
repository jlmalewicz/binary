
import xspec
import matplotlib.pyplot as plt
import accretion_definitions as acc


colors = ['#DA674D', '#1AAD85','k']

xspec.AllModels.lmod("relxill",dirPath="/localdata/relxill")
xspec.AllData.dummyrsp(lowE = 0.02, highE = 200, nBins = 2000, scaleType = 'log')

# primary
bh1 = xspec.Model("phabs*cflux*zashift*relxilllpCp", "bh1")
bh1.setPars({1: 0.03},{2: 2},{3: 10},{4: -10.03},{5: 0.023},
            {6: 30},{7: 0.99},{8: -1},{9: 51.29},{10: 10},
            {11: 0},{12: 2},{13: 2.576},{14: 15},{15: 1},
            {16: 60},{17: 1},{18: 0.1},{19: 0},{20: 2},
            {21: 1},{22: 1},{23: 1}
)

xspec.Plot.device = "/null"
xspec.Plot("eemodel","bh1")

xx = xspec.Plot.x()
y1 = xspec.Plot.model()
ax_labels = xspec.Plot.labels()

bh2 = xspec.Model("phabs*cflux*zashift*relxilllpCp", "bh2")
bh2.setPars({1: 0.03},{2: 2},{3: 10},{4: -10.08},{5: -0.027},
            {6: 30},{7: 0.99},{8: -1},{9: 54.31},{10: 10},
            {11: 0},{12: 2},{13: 2.851},{14: 15},{15: 1},
            {16: 60},{17: 1},{18: 0.1},{19: 0},{20: 2},
            {21: 1},{22: 1},{23: 1}
)


xspec.Plot.device = "/null"
xspec.Plot("eemodel","bh2")

y2 = xspec.Plot.model()

y1y2 = [x + y for x, y in zip(y1, y2)]

###### Plotting
def plot():
    linestyles = ['--', '-.', '-']
    labels = ['Primary:     ', 'Secondary: ', 'Composite']
    q_str     = '{:.1f}'.format(0.9)
    l_tot_str = '{:.2f}'.format(0.1)

    #text = [r'$\lambda_1$ = '+'{:.2g}'.format(data['eddratio'][0])+r', log$_{10}(\xi_1)$ = '+'{:.2f}'.format(data['logxi'][0]), r'$\lambda_2$ = '+'{:.2g}'.format(data['eddratio'][1])+r', log$_{10}(\xi_2)$ = '+'{:.2f}'.format(data['logxi'][1]), r'$\lambda_{\rm tot}$ = '+l_tot_str]


    fig = plt.figure(figsize=(7, 5), dpi=100)
    plt.xlim(0.2,150)


    # x-values are the energy, same for all 3 inputs
    for x, y, linsty, col in zip([xx,xx,xx], [y1, y2,y1y2], linestyles, colors):
        plt.plot(x,y, ls = linsty, c = col, linewidth=1.2)
    #plt.legend(loc="upper left")
    plt.xlabel(ax_labels[0], fontsize=14)
    plt.ylabel(ax_labels[1], fontsize=14)

    

    plt.xscale('log')
    plt.title('q = '+q_str+r', $\lambda_{\rm tot}$ = '+l_tot_str+', phase = '+r'$90^{\circ}$')
    plt.grid(True, which='minor', alpha=0.4, ls='--', linewidth=0.5)
    plt.grid(True, which='major', alpha=0.6, linewidth=0.8)
    plt.tight_layout()
    plt.show()

plot()
