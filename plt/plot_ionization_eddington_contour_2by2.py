'''
2 by 2 grid contour plot of logxi for both 1 and 2
as a function of mass ratio (q) and at what value 
we have set the limiting Eddington ratio
'''

import matplotlib.pyplot as plt
import numpy as np
import accretion_definitions as acc
import matplotlib.colors as colors

fixed_lambda_value = np.logspace(-2,0,50)

q = np.logspace(-1.58, 0, num=50)
# Farris+2014 uses values of q between 0.026 and 1
M = 1e7 #Msun

Q,L = np.meshgrid(q, fixed_lambda_value)

fig, [[ax11, ax12], [ax21, ax22]] = plt.subplots(2, 2, figsize=(12,10), layout='tight')

Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = acc.get_all_mdot('total', L, Q, M)
    
xi_1 = np.ones_like(Q)
xi_2 = np.ones_like(Q)

for plotwhat, ax1, ax2 in zip(['lambda', 'logxi'], [ax11,ax12], [ax21, ax22]):
# slow (~10s), because loops over every value independently
# but this'll do for now
    if plotwhat == 'lambda':
        #for i in np.arange(len(q)):
        #    for j in np.arange(len(q)):
        #        xi_1[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i,j]))
        #        xi_2[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[i,j]))

        loglambdamin=np.log10(0.01)#(min(lambda_1.min(), lambda_2.min()))
        loglambdamax=np.log10(1)#(max(lambda_1.min(), lambda_2.max()))

        loglambda_levels = np.linspace(loglambdamin, loglambdamax, 15)
        lambda_ticks = ['{:.2g}'.format(10**x) for x in list(loglambda_levels)]

        CS11 = ax11.contourf(Q, L, np.log10(lambda_1), cmap='magma', levels=loglambda_levels, vmin=-2, vmax=0, extend='both')
        cb1 = fig.colorbar(CS11, ax=ax11)
        cb1.ax.set_yticklabels(lambda_ticks)

        CS21 = ax21.contourf(Q, L, np.log10(lambda_2), cmap='magma',  levels=loglambda_levels, vmin=-2, vmax=0, extend='both')
        cb2 = fig.colorbar(CS21, ax=ax21)
        cb2.ax.set_yticklabels(lambda_ticks)

    elif plotwhat == 'logxi':
        for i in np.arange(len(q)):
            for j in np.arange(len(q)):
                xi_1[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i,j]))
                xi_2[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[i,j]))
                
        CS12 = ax12.contourf(Q, L, np.log10(xi_1), levels=15, extend='max')
        fig.colorbar(CS12, ax=ax12)

        CS22 = ax22.contourf(Q, L, np.log10(xi_2), CS12.levels, extend='max')
        fig.colorbar(CS22, ax=ax22)
    
    qs = [0.2,  0.2, 0.5,  0.5, 0.5, 0.9,  0.9, 0.9]
    ls = [0.05, 0.1, 0.05, 0.1, 0.5, 0.05, 0.1, 0.5]

    ax1.scatter(qs, ls, color='w', edgecolor='k', s = 20)
    ax2.scatter(qs, ls, color='w', edgecolor='k', s = 20)

for ax in [ax11,ax12,ax21,ax22]:
    ax.set_yscale('log')

for ax in [ax11,ax21]:
    ax.set_ylabel(r'Choice of Eddington ratio $\lambda_{\rm tot}$')

for ax in [ax21, ax22]:
    ax.set_xlabel(r"Mass ratio $q = m_2/m_1$")


ax11.set_title(r'Eddington ratio $\lambda_1$')
ax21.set_title(r'Eddington ratio $\lambda_2$')

ax12.set_title(r'Ionization log$_{10}(\xi_1)$')
ax22.set_title(r'Ionization $log_{10}(\xi_2)$')

plt.show()