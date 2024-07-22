'''
this the real meat
'''


import glob
import xspec # type: ignore
import matplotlib.pyplot as plt
import json
import argparse
import accretion_definitions as acc


parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="if filename given, take it lol", default=None)
args = parser.parse_args()

if args.filename is None:
    for file in glob.glob("*.json"):
        with open(file, 'r') as f:
            data = json.load(f)

else:
    with open(args.filename, 'r') as f:
            data = json.load(f)



xspec.AllModels.lmod("relxill",dirPath="~/work/relxill")

xspec.AllData.dummyrsp(lowE = data['xspec:energylim'][0], highE = data['xspec:energylim'][1], nBins = int(data['xspec:energylim'][2]), scaleType = 'log')

#################
#               #
#    PRIMARY    #
#               #
#################

i=0

bh1 = xspec.Model("zashift(relxilllpCp)", "bh1")
bh1.setPars({1: data['redshift'][i]},
            {3: data['spin'][i]},
            {5: data['rout'][i]/data['rg'][i]},
            {6: data['height'][i]},
            {9: data['logxi'][i]},
            {16:2},
            {18:1},
            {19: data['area'][i] * data['mdot'][i]}
)

xspec.Plot.device = "/null"
xspec.Plot("eemodel","bh1")

xx = xspec.Plot.x()
y1 = xspec.Plot.model()
ax_labels = xspec.Plot.labels()



#################
#               #
#   SECONDARY   #
#               #
#################

i=1

bh2 = xspec.Model("zashift(relxilllpCp)", "bh2")
bh2.setPars({1: data['redshift'][i]},
            {3: data['spin'][i]},
            {5: data['rout'][i]/data['rg'][i]},
            {6: data['height'][i]},
            {9: data['logxi'][i]},
            {16:2},
            {18:1},
            {19: data['area'][i] * data['mdot'][i]}
)

xspec.Plot.device = "/null"
xspec.Plot("eemodel","bh2")

y2 = xspec.Plot.model()


#################
#               #
#   COMPOSITE   #
#               #
#################

y1y2 = [x + y for x, y in zip(y1, y2)]

###### Plotting
def plot():
    linestyles = ['--', ':', '-']
    labels = ['Primary:     ', 'Secondary: ', 'Composite']
    q_str     = '{:.1f}'.format(data['mass ratio'])
    l_tot_str = '{:.2f}'.format(data['eddratio'][2])

    text = [r'$\lambda_1$ = '+'{:.2g}'.format(data['eddratio'][0])+r', log$_{10}(\xi_1)$ = '+'{:.2f}'.format(data['logxi'][0]), r'$\lambda_2$ = '+'{:.2g}'.format(data['eddratio'][1])+r', log$_{10}(\xi_2)$ = '+'{:.2f}'.format(data['logxi'][1]), r'$\lambda_{\rm tot}$ = '+l_tot_str]

    ftsize = data['settings:fontsize']
    lwidth = data['settings:linewidth']

    if data['settings:focus'] == 'feka':
         fig = plt.figure(figsize=(4, 9), dpi=100)
         xmin, xmax = 6.2, 7.2
         plt.xlim(xmin, xmax)
         ymin, ymax = acc.find_corresponding_y_lim(xx,y1,y2,y1y2,xmin,xmax)
         plt.ylim(ymin, ymax)
    elif data['settings:focus'] == 'custom':
         xmin, xmax, ymin, ymax = data['settings:lim']
         fig = plt.figure(figsize=(7, 5), dpi=100)
         plt.xlim(xmin,xmax)
         plt.ylim(ymin,ymax)
         plt.xticks(fontsize=ftsize)
         plt.tick_params(axis='x', which='minor', labelsize=10)
         plt.yticks(fontsize=ftsize)

         
    else:
         fig = plt.figure(figsize=(7, 5), dpi=100)
         plt.xlim(0.1, 70)
         plt.xticks(fontsize=ftsize)
         plt.tick_params(axis='x', which='minor', labelsize=10)
         plt.yticks(fontsize=ftsize)


    # x-values are the energy, same for all 3 inputs
    for x, y, lab, linsty, col, tex in zip([xx,xx,xx], [y1, y2,y1y2], labels, linestyles, data['settings:colors'], text):
        plt.plot(x,y,  label = tex, ls = linsty, c = col, linewidth=lwidth)
    #plt.legend(loc="upper left")
    plt.xlabel(ax_labels[0], fontsize=ftsize)
    plt.ylabel(ax_labels[1], fontsize=ftsize)

    

    plt.xscale('log')
    plt.title('q = '+q_str+r', $\lambda_{\rm tot}$ = '+l_tot_str+', phase = '+data['phase']+r'$^{\circ}$')
    plt.grid(True, which='minor', alpha=0.4, ls='--', linewidth=0.5)
    plt.grid(True, which='major', alpha=0.6, linewidth=0.8)
    plt.tight_layout()
    if data['settings:savefig']:
        plt.savefig("~/work/img/"+data['settings:imageloc']+"/composite_spectrum_"+data['settings:filename']+".png")
    plt.show()

plot()