'''
Double contour plot of logxi for both 1 and 2
as a function of mass ratio (q) and at what value 
we have set the limiting Eddington ratio,
only plot region where both are in relxill
range
'''

import matplotlib.pyplot as plt
import numpy as np
import accretion_definitions as acc
import seaborn as sns
import pandas as pd
import matplotlib.colors as colors

fixed_lambda_value = np.logspace(-2,0,50)
q = np.logspace(-1.58, 0, num=50)
M = 1e7

Q,L = np.meshgrid(q, fixed_lambda_value)

Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = acc.get_all_mdot('total', L, Q, M)
    

mask_1 = np.ones_like(Q)
mask_2 = np.ones_like(Q)

mask_1 = (lambda_1 >= 0.01) & (lambda_1 <= 1)
mask_2 = (lambda_2 >= 0.01) & (lambda_2 <= 1)

masked_lambda_1 = np.where(mask_1, (lambda_1), np.nan)
masked_lambda_2 = np.where(mask_2, (lambda_2), np.nan)

lambdamin=0.01
lambdamax=1


#lambda_levels = np.logspace(-2, 0, 9)
lambda_levels = np.asarray([0.01, 0.02, 0.05, 0.1, 0.2, 0.5,1])
lambda_ticks = ['{:.2g}'.format(x) for x in list(lambda_levels)]

""" CS1 = ax1.contourf(Q, L, (masked_lambda_1), cmap='magma', levels=lambda_levels)
cb1 = fig.colorbar(CS1, ax=ax1)
cb1.ax.set_yticklabels(lambda_ticks)

CS2 = ax2.contourf(Q, L, (masked_lambda_2), cmap='magma',  levels=lambda_levels)
cb2 = fig.colorbar(CS2, ax=ax2)
cb2.ax.set_yticklabels(lambda_ticks) """

fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(6,10), layout='tight')

plt.rcParams['axes.grid'] = False

lognorm = colors.LogNorm(vmin=lambdamin, vmax=lambdamax)


cm1 = ax1.pcolormesh(Q, L, masked_lambda_1, cmap='magma', norm=lognorm)
c1 =  ax1.contour(Q, L, masked_lambda_1, colors='yellow', levels = list(lambda_levels))

""" cb1 = fig.colorbar(c1, ax=ax1, ticks = lambda_ticks)
cb1.ax.set_yticklabels(lambda_ticks)

ax1.clabel(c1, c1.levels, inline=True, fontsize=10) """



ax1.set_title(r'Eddington ratio $\lambda_1$')
ax2.set_title(r'Eddington ratio $\lambda_2$')

for ax in [ax1,ax2]:
    ax.set_yscale('log')
    ax.set_ylabel(r'Choice of Eddington ratio $\lambda_{\rm tot}$')
    ax.set_xlabel(r"Mass ratio $q = m_2/m_1$")

""" qs = [0.2, 0.2, 0.2, 0.5, 0.5, 0.5, 0.9, 0.9, 0.9]
ls = [0.05, 0.1, 0.5] * 3

ax1.scatter(qs, ls, c='w', edgecolors='k')
ax2.scatter(qs, ls, c='w', edgecolors='k')
 """
#fig.suptitle(r'Region where both $\xi_1$ and $\xi_2$ ' + 'are\nwithin relxill bounds ' +r'(0<log$_{10}(\xi)<4.7$)')

plt.show()