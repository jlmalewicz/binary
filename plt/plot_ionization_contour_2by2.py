'''
2 by 2 grid contour plot of logxi for both 1 and 2
as a function of mass ratio (q) and at what value 
we have set the limiting Eddington ratio

          | total   | secondary |
          | limited | limited   |
----------|---------|-----------|
primary   |         |           |
----------|---------|-----------|
secondary |         |           |
----------|---------|-----------|
'''

import matplotlib.pyplot as plt
import numpy as np
import accretion_definitions as acc

fixed_lambda_value = np.logspace(-2,0,50)

q = np.logspace(-1.58, 0, num=50)
# Farris+2014 uses values of q between 0.026 and 1
M = 1e7 #Msun

Q,L = np.meshgrid(q, fixed_lambda_value)

fig, [[ax11, ax12], [ax21, ax22]] = plt.subplots(2, 2, figsize=(12,10), layout='tight')


for fixed_lambda, ax1, ax2 in zip(['total', 'secondary'], [ax11,ax12], [ax21, ax22]):
    Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = acc.get_all_mdot(fixed_lambda, L, Q, M)
    
    xi_1 = np.ones_like(Q)
    xi_2 = np.ones_like(Q)

# slow (~10s), because loops over every value independently
# but this'll do for now
    if fixed_lambda == 'total':
        for i in np.arange(len(q)):
            for j in np.arange(len(q)):
                xi_1[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i,j]))
                xi_2[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[i,j]))

        CS11 = ax11.contourf(Q, L, np.log10(xi_1))
        fig.colorbar(CS11, ax=ax11, label=r'log $\xi$')

        CS21 = ax21.contourf(Q, L, np.log10(xi_2), CS11.levels)
        fig.colorbar(CS21, ax=ax12, label=r'log $\xi$')

    elif fixed_lambda == 'secondary':
        for i in np.arange(len(q)):
            for j in np.arange(len(q)):
                xi_1[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i,j]))
                xi_2[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[i,j]))
                
        CS12 = ax12.contourf(Q, L, np.log10(xi_1), CS11.levels)
        fig.colorbar(CS12, ax=ax21, label=r'log $\xi$')

        CS22 = ax22.contourf(Q, L, np.log10(xi_2), CS11.levels)
        fig.colorbar(CS22, ax=ax22, label=r'log $\xi$')



for ax in [ax11,ax12,ax21,ax22]:
    ax.set_xlabel(r"Mass ratio $q = m_2/m_1$")
    ax.set_yscale('log')

# Total accretion limited
for ax in [ax11,ax21]:
    ax.set_ylabel(r'Eddington ratio $\lambda_{\rm tot}$ for the TOTAL system')
    ax.set_title('Total accretion limited')
# Accretion of secondary limited
for ax in [ax12,ax22]:
    ax.set_ylabel(r'Eddington ratio $\lambda_{2}$ for the secondary')
    ax.set_title('Accretion of secondary limited')

plt.show()