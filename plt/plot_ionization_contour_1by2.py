import matplotlib.pyplot as plt
import numpy as np
import bin.accretion_definitions as acc

fixed_lambda_values = np.logspace(-2,0, num = 50)
#q = np.logspace(-1.58, 0, num = 50)
q = np.linspace(0.026, 1, num = 50)
# Farris+2014 uses values of q between 0.026 and 1
M = 1e7 #Msun


Q,L = np.meshgrid(q, fixed_lambda_values)
Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = acc.get_all_mdot('total', L, Q, M)

xi_1 = np.ones_like(lambda_1)
xi_2 = np.ones_like(lambda_2)

Qi = np.ones_like(lambda_1)

for i in np.arange(len(q)):
    Qi[i] = q[i] * np.ones_like(lambda_1[i,:])

    for j in np.arange(len(lambda_1[i,:])):
        xi_1[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd = np.log10(lambda_1[i,j]))
        xi_2[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd = np.log10(lambda_2[i,j]))

logxi_1 = np.log10(xi_1)
logxi_2 = np.log10(xi_2)

min_logxi = np.min([np.min(logxi_1), np.min(logxi_2)])
max_logxi = np.max([np.max(logxi_1), np.max(logxi_2)])

min_lambda = np.min([np.min(lambda_1), np.min(lambda_2)])
max_lambda = np.max([np.max(lambda_1), np.max(lambda_2)])


fig, [ax1, ax2] = plt.subplots(1, 2, figsize = (12,5), layout='tight') 

scat1 = ax1.scatter(Qi.flatten(), (lambda_1.flatten()), c = logxi_1.flatten(), cmap = 'viridis', vmin=min_logxi, vmax=max_logxi, label = r'Primary $m_1$')
scat2 = ax2.scatter(Qi.flatten(), (lambda_2.flatten()), c = logxi_2.flatten(), cmap = 'viridis', vmin=min_logxi, vmax=max_logxi, label = r'Secondary $m_2=qm_1$')

for ax in [ax1,ax2]:
    ax.legend(loc = 'best')
    ax.set_ylim([min_lambda, max_lambda])
    ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.set_xlabel(r'Mass ratio $q$')
    ax.set_ylabel(r'Rate of accretion as fraction of Eddington $\lambda$')



fig.colorbar(scat2, label = r'log$(\xi)$')

plt.show()
