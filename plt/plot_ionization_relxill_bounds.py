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

fixed_lambda_value = np.logspace(-2,0,50)
q = np.logspace(-1.58, 0, num=50)
M = 1e7

#plotwhat = 'Eddington'
plotwhat = 'logxi'

relxill_bounds = [0, 4.7]

Q,L = np.meshgrid(q, fixed_lambda_value)

Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = acc.get_all_mdot('total', L, Q, M)
    
xi_1 = np.ones_like(Q)
xi_2 = np.ones_like(Q)
mask = np.ones_like(Q)

for i in np.arange(len(q)):
    for j in np.arange(len(q)):
        xi_1[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i,j]))
        xi_2[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[i,j]))      

mask = (xi_1 > 1) & (xi_1 < 10**4.7) & (xi_2 > 1) & (xi_2 < 10**4.7)

fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(6,10), layout='tight')

if plotwhat == 'logxi':
    CS1 = ax1.contourf(Q, L, np.where(mask, np.log10(xi_1), np.nan))
    fig.colorbar(CS1, ax=ax1)

    CS2 = ax2.contourf(Q, L, np.where(mask, np.log10(xi_2), np.nan), CS1.levels)
    fig.colorbar(CS2, ax=ax2)

    ax1.set_title(r'Ionization log$_{10}(\xi_1)$')
    ax2.set_title(r'Ionization log$_{10}(\xi_2)$')

if plotwhat == 'Eddington':

    mask_lambda_1 = np.where(mask, (lambda_1), np.nan)
    mask_lambda_2 = np.where(mask, (lambda_2), np.nan)
    
    loglambdamin=np.log10(min(np.nanmin(mask_lambda_1), np.nanmin(mask_lambda_2)))
    loglambdamax=np.log10(max(np.nanmax(mask_lambda_2), np.nanmax(mask_lambda_2)))

    loglambda_levels = np.linspace(loglambdamin, loglambdamax, 10)
    lambda_ticks = ['{:.2g}'.format(10**x) for x in list(loglambda_levels)]

    CS1 = ax1.contourf(Q, L, np.log10(mask_lambda_1), cmap='magma', levels=loglambda_levels)
    cb1 = fig.colorbar(CS1, ax=ax1)
    cb1.ax.set_yticklabels(lambda_ticks)

    CS2 = ax2.contourf(Q, L, np.log10(mask_lambda_2), cmap='magma',  levels=loglambda_levels)
    cb2 = fig.colorbar(CS2, ax=ax2)
    cb2.ax.set_yticklabels(lambda_ticks)
    
    ax1.set_title(r'Eddington ratio $\lambda_1$')
    ax2.set_title(r'Eddington ratio $\lambda_2$')

for ax in [ax1,ax2]:
    ax.set_yscale('log')
    ax.set_ylabel(r'Choice of Eddington ratio $\lambda_{\rm tot}$')
    ax.set_xlabel(r"Mass ratio $q = m_2/m_1$")

qs = [0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.5, 0.7, 0.7, 0.7, 0.7, 0.9, 0.9, 0.9, 0.9]
ls = [0.02, 0.05, 0.1, 0.15] * 5

ax1.scatter(qs, ls)
ax2.scatter(qs, ls)

fig.suptitle(r'Region where both $\xi_1$ and $\xi_2$ ' + 'are\nwithin relxill bounds ' +r'(0<log$_{10}(\xi)<4.7$)')

plt.show()